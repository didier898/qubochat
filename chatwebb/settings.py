import os
# Importa la configuración de JWT
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'your_secret_key_here'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'rest_framework',
    'drf_yasg',
    'rest_framework_simplejwt',
    'corsheaders',
    'core',
  
]

# Configuración de JWT
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=8000),  # Tiempo de vida del token de acceso
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=50),  # Tiempo de vida del token de actualización
    'SLIDING_TOKEN_LIFETIME': timedelta(days=7),  # Tiempo de vida del token de actualización
    'SLIDING_TOKEN_REFRESH_LIFETIME_GRACE_PERIOD': timedelta(days=2),  # Período de gracia para la actualización del token
    'SLIDING_TOKEN_REFRESH_EACH_TIME': True,  # Actualizar el token en cada solicitud
    'ROTATE_REFRESH_TOKENS': False,  # Rotar tokens de actualización
    'ALGORITHM': 'HS256',  # Algoritmo de firma del token
    'SIGNING_KEY': SECRET_KEY,  # Clave secreta para firmar el token
    'VERIFYING_KEY': None,  # Clave de verificación (dejar en None para usar SIGNING_KEY)
    'AUTH_HEADER_TYPES': ('Bearer',),  # Tipos de encabezado de autenticación
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),  # Clases de token de autenticación
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

APPEND_SLASH = False

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'es-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

AUTH_USER_MODEL = 'core.UserProfile'
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://192.168.1.14:3000',
    
]

CORS_ALLOW_ALL_ORIGINS = True  # Esto permite todas las solicitudes, pero debe restringirse en producción.

