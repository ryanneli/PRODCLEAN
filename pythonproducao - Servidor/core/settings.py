import os

from pathlib import Path



# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = 'django-insecure-130@+z78ohlrt_#5&$(v=vvt(15+q5nj!x_-jc*@rfwo7kb#$!'



DEBUG = False



ALLOWED_HOSTS = ['192.168.50.100', 'eletroinoxproducao.com', 'localhost', '127.0.0.1', '*']  # O asterisco libera qualquer Host/IP



CSRF_TRUSTED_ORIGINS = [

    'http://eletroinoxproducao.com',

    'http://www.eletroinoxproducao.com',

    'https://eletroinoxproducao.com',

    'https://www.eletroinoxproducao.com',

    'http://192.168.50.100',

    'https://192.168.50.100',

    'http://192.168.50.100:8080',
 
    'https://192.168.50.100:8080',

    'http://localhost:8080',
]

# Application definition



INSTALLED_APPS = [
    'daphne',

    'django.contrib.admin',

    'django.contrib.auth',

    'django.contrib.contenttypes',

    'django.contrib.sessions',

    'django.contrib.messages',

    'django.contrib.staticfiles',

    'producao',

    'rangefilter',

    'channels',

]



MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware', 

    'django.contrib.sessions.middleware.SessionMiddleware', # Apenas uma vez

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

        'DIRS': [],

        'APP_DIRS': True,

        'OPTIONS': {

            'context_processors': [

                'django.template.context_processors.request',

                'django.contrib.auth.context_processors.auth',

                'django.contrib.messages.context_processors.messages',

		'producao.context_processors.chat_context_processor',

            ],

        },

    },

]



WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    },
}


DATABASES = {

    'default': {

        'ENGINE': 'mssql',

        'NAME': 'novo_banco_Teste',

        'USER': 'sa',

        'PASSWORD': 'admin1270',

        'HOST': '192.168.50.100', 

        'PORT': '1433',

        'CONN_MAX_AGE': 600,

        'OPTIONS': {

            'driver': 'ODBC Driver 17 for SQL Server',

            'extra_params': 'TrustServerCertificate=yes',

        },

    }

}





# Password validation

# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators



AUTH_PASSWORD_VALIDATORS = []




# Internationalization

# https://docs.djangoproject.com/en/6.0/topics/i18n/







USE_I18N = True



TIME_ZONE = 'America/Sao_Paulo'



# Garante que o Django use o fuso horário definido acima

USE_TZ = True



# Opcional: define o idioma das datas para português

LANGUAGE_CODE = 'pt-br'





# Static files (CSS, JavaScript, Images)

# https://docs.djangoproject.com/en/6.0/howto/static-files/



STATIC_URL = 'static/'

LOGIN_URL = 'login' 

LOGIN_REDIRECT_URL = 'dashboard'

LOGOUT_REDIRECT_URL = 'login'





SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')





SESSION_COOKIE_SECURE = False



CSRF_COOKIE_SECURE = False





SESSION_EXPIRE_AT_BROWSER_CLOSE = True



# Define um tempo de inatividade (em segundos). Ex: 3600 = 1 hora

SESSION_COOKIE_AGE = 3600 



# Garante que a sessão seja renovada a cada requisição (evita deslogar enquanto trabalha)

SESSION_SAVE_EVERY_REQUEST = True







MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



STATIC_URL = '/static/'

STATICFILES_DIRS = [

    os.path.join(BASE_DIR, 'static')

]



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Onde o Django vai 'jogar' todos os arquivos prontos para o servidor

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')



#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'