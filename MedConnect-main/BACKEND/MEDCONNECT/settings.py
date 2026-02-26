import os
from pathlib import Path
import dj_database_url

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-(#)bsn2e644+wxx!omuv-z+bn5%k2gc_bpn$4$qgpb8*l5#vbb')

# SET TO FALSE FOR PRODUCTION
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Add your Render URL and Netlify URL here
ALLOWED_HOSTS = [
    'localhost', 
    '127.0.0.1', 
    '.onrender.com',  # Allows all Render subdomains
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'medconnect_app', 
]



ROOT_URLCONF = 'MEDCONNECT.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'MEDCONNECT.wsgi.application'

import os
from urllib.parse import urlparse

if os.environ.get('DATABASE_URL'):
    # Manually parse the URL to avoid helper library errors
    url = urlparse(os.environ.get('DATABASE_URL'))
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': url.path[1:],
            'USER': url.username,
            'PASSWORD': url.password,
            'HOST': url.hostname,
            'PORT': url.port,
            'OPTIONS': {
                'ssl': {'ca': None}, # Use SSL but skip cert verification
            }
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- SECURITY & HTTPS (Required for Render) ---
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# This ensures cookies work across different domains (Netlify -> Render)
CORS_ALLOW_CREDENTIALS = True

if not DEBUG:
    # Production Settings (Render/Netlify)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = 'None' 
    CSRF_COOKIE_SAMESITE = 'None'    
    SECURE_SSL_REDIRECT = True
else:
    # Local Settings (Development)
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = 'Lax'
    CSRF_COOKIE_SAMESITE = 'Lax'

# --- CORS & ORIGINS ---
# Uses Environment Variables from Render, but defaults to localhost for your computer
FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:5173').rstrip('/')
BACKEND_URL = os.environ.get('BACKEND_URL', 'http://localhost:8000').rstrip('/')

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    FRONTEND_URL,
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:8000",
    FRONTEND_URL,
    BACKEND_URL,
]

# --- MIDDLEWARE (Ensure CorsMiddleware is #1) ---
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --- REMAINING SETTINGS ---
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'