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

# Application definition

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

# CHANNEL_LAYERS = {
#     'default': {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [("127.0.0.1", 6379)],
#         },
#     }
# }

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

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

LOGIN_REDIRECT_URL = '/select_user_type/'
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
        }
    },
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
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
            'updated_time',
        ],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': lambda request: 'ru_RU',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v13.0',
    },
}


SOCIALACCOUNT_QUERY_EMAIL = True

# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
# }
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

ACCOUNT_LOGOUT_REDIRECT_URL = '/'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False


AUTH_USER_MODEL = "authentication.User"

AUTHENTICATION_BACKENDS = (
   'django.contrib.auth.backends.ModelBackend',
   'allauth.account.auth_backends.AuthenticationBackend'
)



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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# STATIC_ROOT = os.path.join(BASE_DIR, "apps/static")
STATIC_URL = "/static/"

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (os.path.join(BASE_DIR, "apps/static"),)

MEDIA_ROOT = os.path.join(BASE_DIR, "apps/media")
MEDIA_URL = "/media/"

CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", default="").split(',')

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
#
# JAZZMIN_SETTINGS = {
#     # title of the window (Will default to current_admin_site.site_title if absent or None)
#     "site_title": "MeeBuy",
#
#     # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
#     "site_header": "MeeBuy",
#
#     # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
#     "site_brand": "MeeBuy",
#
#     # Logo to use for your site, must be present in static files, used for brand on top left
#     "site_logo": "logo/logo.png",
#
#     # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
#     "login_logo": 'logo/logo.png',
#
#     # Logo to use for login form in dark themes (defaults to login_logo)
#     "login_logo_dark": 'logo/logo.png',
#
#     # CSS classes that are applied to the logo above
#     "site_logo_classes": "img-cube",
#
#     # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
#     "site_icon": 'logo/logo.png',
#
#     # Welcome text on the login screen
#     "welcome_sign": _("Добро пожаловать!"),
#
#     # Copyright on the footer
#     "copyright": "Acme Library Ltd",
#
#     # List of model admins to search from the search bar, search bar omitted if excluded
#     # If you want to use a single search field you dont need to use a list, you can use a simple string
#     "search_model": ["auth.User", "auth.Group"],
#
#     # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
#     "user_avatar": None,
#
#     ############
#     # Top Menu #
#     ############
#
#     # Links to put along the top menu
#     "topmenu_links": [
#
#         # Url that gets reversed (Permissions can be added)
#         {"name": _("Домой"), "url": "admin:index", "permissions": ["auth.view_user"]},
#
#         # external url that opens in a new window (Permissions can be added)
#         {"name": _("Поддержка"), "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
#
#         # model admin to link to (Permissions checked against model)
#         {"model": "authentication.User"},
#
#         # App with dropdown menu to all its models pages (Permissions checked against models)
#         {"app": "announcement"},
#     ],
#
#     #############
#     # User Menu #
#     #############
#
#     # Additional links to include in the user menu on the top right ("app" url type is not allowed)
#     "usermenu_links": [
#         {"name": _("Поддержка"), "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
#         {"model": "authentication.User"}
#     ],
#
#     #############
#     # Side Menu #
#     #############
#
#     # Whether to display the side menu
#     "show_sidebar": True,
#
#     # Whether to aut expand the menu
#     "navigation_expanded": True,
# # Hide these apps when generating side menu e.g (auth)
#     "hide_apps": [],
#
#     # Hide these models when generating side menu (e.g auth.user)
#     "hide_models": [],
#
#     # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
#     "order_with_respect_to": ["authentication.User", "auth.Group", "category.Category", "category.SubCategory"],
#
#     # Custom links to append to app groups, keyed on app name
#     # "custom_links": {
#     #     "announcement": [{
#     #         "name": "Make Messages",
#     #         "url": "make_messages",
#     #         "icon": "fas fa-comments",
#     #         "permissions": ["announcement.view_book"]
#     #     }]
#     # },
#
#     # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
#     # for the full list of 5.13.0 free icon classes
#     "icons": {
#         "auth": "fas fa-users-cog",
#         "auth.User": "fas fa-user",
#         "auth.Group": "fas fa-users",
#     },
#     # Icons that are used when one is not manually specified
#     "default_icon_parents": "fas fa-chevron-circle-right",
#     "default_icon_children": "fas fa-circle",
#
#     #################
#     # Related Modal #
#     #################
#     # Use modals instead of popups
#     "related_modal_active": False,
#
#     #############
#     # UI Tweaks #
#     #############
#     # Relative paths to custom CSS/JS scripts (must be present in static files)
#     "custom_css": None,
#     "custom_js": None,
#     # Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)
#     "use_google_fonts_cdn": True,
#     # Whether to show the UI customizer on the sidebar
#
#     ###############
#     # Change view #
#     ###############
#     # Render out the change view as a single form, or in tabs, current options are
#     # - single
#     # - horizontal_tabs (default)
#     # - vertical_tabs
#     # - collapsible
#     # - carousel
#     "changeform_format": "horizontal_tabs",
#     # override change forms on a per modeladmin basis
#     "changeform_format_overrides": {"authentication.User": "collapsible", "auth.Group": "vertical_tabs"},
# }



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
