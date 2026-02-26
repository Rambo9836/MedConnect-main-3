import json
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Profile, PatientProfile, ResearcherProfile

# 1. HELPER: Standardize User Data for React
def get_user_data(user, role):
    return {
        'id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'role': role
    }

# 2. HELPER: Standardize Auth Check for API (Fixes 401 Errors)
def api_login_check(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Not authenticated'}, status=401)
    return None

@csrf_exempt
def home(request):
    return JsonResponse({"message": "MedConnect API is running", "status": "success"})

@csrf_exempt
def patient_register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            
            # Prevent duplicate emails
            if User.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'message': 'Email already registered.'}, status=400)

            user = User.objects.create_user(
                username=data.get('username'),
                email=email,
                password=data.get('password'),
                first_name=data.get('first_name'),
                last_name=data.get('last_name')
            )
            
            # Ensure Profile exists and set role
            profile, created = Profile.objects.get_or_create(user=user)
            profile.role = 'patient'
            profile.save()
            
            PatientProfile.objects.create(
                profile=profile,
                date_of_birth=data.get('date_of_birth'),
                gender=data.get('gender'),
                cancer_type=data.get('cancer_type'),
                phone_number=data.get('phone_number')
            )
            
            login(request, user)
            return JsonResponse({'success': True, 'user': get_user_data(user, 'patient')})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
    return JsonResponse({'message': 'Method not allowed'}, status=405)

@csrf_exempt
def researcher_register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')

            if User.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'message': 'Email already registered.'}, status=400)

            user = User.objects.create_user(
                username=data.get('username'),
                email=email,
                password=data.get('password'),
                first_name=data.get('first_name'),
                last_name=data.get('last_name')
            )
            
            profile, created = Profile.objects.get_or_create(user=user)
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
            return JsonResponse({'success': True, 'user': get_user_data(user, 'researcher')})
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
            
            user = authenticate(username=username_or_email, password=password)
            
            if user is None:
                user_obj = User.objects.filter(email=username_or_email).first()
                if user_obj:
                    user = authenticate(username=user_obj.username, password=password)
            
            if user is not None:
                login(request, user)
                # Safeguard against users missing profiles
                profile, created = Profile.objects.get_or_create(user=user)
                return JsonResponse({'success': True, 'user': get_user_data(user, profile.role)})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid credentials'}, status=401)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
    return JsonResponse({'message': 'Method not allowed'}, status=405)

@csrf_exempt
def user_logout(request):
    logout(request)
    return JsonResponse({'success': True, 'message': 'Logged out'})

@csrf_exempt
def get_profile(request):
    # Use helper to return 401 instead of HTML redirect
    auth_error = api_login_check(request)
    if auth_error: return auth_error

    user = request.user
    try:
        profile, created = Profile.objects.get_or_create(user=user)
        role = getattr(profile, 'role', 'patient')
        return JsonResponse({
            'success': True,
            'user': get_user_data(user, role)
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@csrf_exempt
def api_user_info(request):
    # Route back to profile logic
    return get_profile(request)