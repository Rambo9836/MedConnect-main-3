import json
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Profile, PatientProfile, ResearcherProfile

# Helper to format user data for React
def get_user_data(user, role):
    return {
        'id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'role': role
    }

@csrf_exempt
def patient_register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Create User
            user = User.objects.create_user(
                username=data.get('username'),
                email=data.get('email'),
                password=data.get('password'),
                first_name=data.get('first_name'),
                last_name=data.get('last_name')
            )
            
            # Update Profile (Role)
            profile = user.profile
            profile.role = 'patient'
            profile.save()
            
            # Create Patient Profile
            PatientProfile.objects.create(
                profile=profile,
                date_of_birth=data.get('date_of_birth'),
                gender=data.get('gender'),
                cancer_type=data.get('cancer_type'),
                phone_number=data.get('phone_number')
            )
            
            login(request, user)
            return JsonResponse({
                'success': True, 
                'message': 'Registration successful',
                'user': get_user_data(user, 'patient')
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
    return JsonResponse({'message': 'Method not allowed'}, status=405)

@csrf_exempt
def researcher_register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = User.objects.create_user(
                username=data.get('username'),
                email=data.get('email'),
                password=data.get('password'),
                first_name=data.get('first_name'),
                last_name=data.get('last_name')
            )
            
            profile = user.profile
            profile.role = 'researcher'
            profile.save()
            
            ResearcherProfile.objects.create(
                profile=profile,
                title=data.get('title'),
                institution=data.get('institution'),
                specialization=data.get('specialization'),
                phone_number=data.get('phone_number')
            )
            
            login(request, user)
            return JsonResponse({
                'success': True, 
                'message': 'Registration successful',
                'user': get_user_data(user, 'researcher')
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
    return JsonResponse({'message': 'Method not allowed'}, status=405)

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username_or_email = data.get('username_or_email')
            password = data.get('password')
            
            # Authenticate via username
            user = authenticate(username=username_or_email, password=password)
            
            # If failed, try via email
            if user is None:
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    user = authenticate(username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None
            
            if user is not None:
                login(request, user)
                return JsonResponse({
                    'success': True, 
                    'user': get_user_data(user, user.profile.role)
                })
            else:
                return JsonResponse({'success': False, 'message': 'Invalid credentials'}, status=401)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
    return JsonResponse({'message': 'Method not allowed'}, status=405)

@csrf_exempt
def user_logout(request):
    logout(request)
    return JsonResponse({'success': True, 'message': 'Logged out'})

@login_required
def get_profile(request):
    user = request.user
    return JsonResponse({
        'success': True,
        'user': get_user_data(user, user.profile.role)
    })