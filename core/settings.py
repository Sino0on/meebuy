import os
from datetime import timedelta
from pathlib import Path
from django.utils.translation import gettext_lazy as _
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", default="S#perS3crEt_1122")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)


ALLOWED_HOSTS = ['*']

# Application definitio makemigrations


PROJECT_APPS = [
    'daphne',
    'channels',
    'simpleui',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.humanize',
    'django.contrib.staticfiles',
    'django.contrib.sites',

]

DJANGO_APPS = [
    'apps.authentication',
    'apps.user_cabinet',
    'apps.provider',
    'apps.chat',
    'apps.tender',
    'apps.product',
    'apps.buyer',
]

THIRD_PARTY_APPS = [
    "django_filters",
    "corsheaders",
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.vk',
    'allauth.socialaccount.providers.yandex',
    'allauth.socialaccount.providers.mailru',



    'rest_framework'
    # 'social.apps.django_app.default',
]

INSTALLED_APPS = [*DJANGO_APPS, *THIRD_PARTY_APPS, *PROJECT_APPS]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    "django.middleware.locale.LocaleMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware'
]


ROOT_URLCONF = 'core.urls'

TEMPLATE_DIR = os.path.join(BASE_DIR, "apps/templates")


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATE_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
            ],
        },
    },
]

ASGI_APPLICATION = 'core.asgi.application'

WSGI_APPLICATION = 'core.wsgi.application'


CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', cast=int),
    }
}
STATIC_ROOT = os.path.join(BASE_DIR, "apps/static")


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
# STATICFILES_DIRS = (os.path.join(BASE_DIR, "apps/static"),)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/


STATIC_URL = "/static/"

# Extra places for collectstatic to find static files.


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

LOGIN_REDIRECT_URL = '/view_profile/'
LOGOUT_REDIRECT_URL = '/'

SITE_ID = int(config("SITE_ID"))


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
    'yandex': {
        'SCOPE': [
            'login:email',
            'login:info',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'mailru': {
            'SCOPE': [
                'login:email',
                'login:info',
            ],
            'AUTH_PARAMS': {
                'access_type': 'online',
            }
        },
        'vk': {
            'SCOPE': [
                'profile',
                'email',
            ],
            'AUTH_PARAMS': {
                'access_type': 'online',
            }
        },
         'facebook': {
                'METHOD': 'oauth2',
                'SCOPE': ['email', 'public_profile'],
                'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
                'FIELDS': [
                    'id',
                    'email',
                    'name',
                    'first_name',
                    'last_name',
                    'verified',
                    'locale',
                    'timezone',
                    'link',
                    'gender',
                    'updated_time'
                ],
                'EXCHANGE_TOKEN': True,
                'LOCALE_FUNC': lambda request: 'en_US',
                'VERIFIED_EMAIL': False,
                'VERSION': 'v7.0',
            }
    },
}


SOCIALACCOUNT_QUERY_EMAIL = True



AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

ACCOUNT_LOGOUT_REDIRECT_URL = '/'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False


AUTH_USER_MODEL = "authentication.User"




# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/


LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Bishkek'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'

MODELTRANSLATION_LANGUAGES = ('ru', 'ky')


MEDIA_ROOT = os.path.join(BASE_DIR, "apps/media")
MEDIA_URL = "/media/"

CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", default="").split(',')

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SOCIALACCOUNT_ADAPTER = 'apps.authentication.adapters.CustomSocialAccountAdapter'
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


SIMPLEUI_HOME_INFO = False
SIMPLEUI_HOME_ACTION = True
SIMPLEUI_HOME_QUICK = True
SIMPLEUI_INDEX = '#'
SIMPLEUI_DEFAULT_THEME = 'e-black-pro.css'
SIMPLEUI_HOME_TITLE = 'Meebuy'
SIMPLEUI_LOGO = '/static/logo/logo.svg'




SIMPLEUI_CONFIG = {
    'system_keep': True,
    'menus': [
        {
            'name': 'Поставщики',
            'icon': 'fa fa-book',
            'models': [
                {
                    'name': 'Поставщики',
                    'icon': 'fa fa-industry',
                    'url': '/dev-admin8/provider/provider/'
                },
                {
                    'name': 'Configurations',
                    'models': [
                        {
                            'name': 'Доставка',
                            'icon': 'fa fa-truck',
                            'url': '/dev-admin8/provider/delivery/'
                        },
                        {
                            'name': 'Категории Поставщиков',
                            'icon': 'fa fa-columns',
                            'url': '/dev-admin8/provider/category/'
                        },
                        {
                            'name': 'Тэги',
                            'icon': 'fa fa-tag',
                            'url': '/dev-admin8/provider/tag/'
                        },
                        {
                            'name': 'Условия',
                            'icon': 'fa fa-table',
                            'url': '/admin/catalog/sizechart/'
                        },
                        {
                            'name': 'Варианты оплаты',
                            'icon': 'fa fa-money-bill',
                            'url': '/dev-admin8/provider/typepay/'
                        },
                    ]
                },
            ]
        },
        {
            'name': 'Товары',
            'icon': 'fa fa-boxes',
            'models': [
                {
                    'name': 'Товары',
                    'icon': 'fa fa-box',
                    'url': '/dev-admin8/product/product/'
                },
                {
                    'name': 'Картнки товаров',
                    'icon': 'fa fa-image',
                    'url': '/dev-admin8/product/productimg/'
                },

            ]
        },
        {
            'name': 'Пользователи',
            'icon': 'fa fa-user',
            'models': [
                {
                    'name': 'Активныйе статусы пользователя',
                    'icon': 'fa fa-circle',
                    'url': '/dev-admin8/user_cabinet/activeuserstatus/'
                },
                {
                    'name': 'Кабинеты',
                    'icon': 'fa fa-image',
                    'url': '/dev-admin8/user_cabinet/cabinet/'
                },
                {
                    'name': 'Статусы',
                    'icon': 'fa fa-info',
                    'url': '/dev-admin8/user_cabinet/status/'
                },
                {
                    'name': 'Статусы пользователей',
                    'icon': 'fa fa-user-secret',
                    'url': '/dev-admin8/user_cabinet/packagestatus/'
                },
                {
                    'name': 'Транзакции',
                    'icon': 'fa fa-play',
                    'url': '/dev-admin8/user_cabinet/transaction/'
                },
            ]
        },
        {
            'name': 'Тендеры',
            'icon': 'fa fa-star',
            'url': '/dev-admin8/tender/tender/'
        },

        {
            'name': 'Локации',
            'icon': 'fa fa-globe',
            'models': [
                {
                    'name': 'Города',
                    'icon': 'fa fa-map-marker',
                    'url': '/dev-admin8/tender/city/'
                },
                {
                    'name': 'Регионы (Области)',
                    'icon': 'fa fa-map',
                    'url': '/dev-admin8/tender/region/'
                },
                {
                    'name': 'Страны',
                    'icon': 'fa fa-flag',
                    'url': '/dev-admin8/tender/country/'
                },

            ]
        },
    ]
}