import os.path
PROJECT_DIR = os.path.dirname(__file__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
	('Jon Taylor', 'jon@sceneshift.com'),
)

MANAGERS = ADMINS

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'sceneshift',
		'USER': 'root',
		'PASSWORD': '',
		'HOST': 'localhost',
		'PORT': '',
	}
}

CACHES = {
	'default': {
		'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
 		'LOCATION': '/Users/jon/Sites/sceneshift/tmp',
	}
}

TIME_ZONE = 'Europe/London'

LANGUAGE_CODE = 'en-gb'
USE_I18N = False
USE_L10N = True

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')
MEDIA_URL = 'http://127.0.0.1:8000/media/'
ADMIN_MEDIA_PREFIX = '/media/admin/'

SECRET_KEY = '$37+nl2sge_@=)+k^i-yz!d!eyk$c#2wzb!gc8lf!8^6d&q+du'

TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'debug_toolbar.middleware.DebugToolbarMiddleware',
	)

INTERNAL_IPS = ('127.0.0.1',)

TEMPLATE_CONTEXT_PROCESSORS = (
	'django.contrib.auth.context_processors.auth',
	'django.core.context_processors.debug',
	'django.core.context_processors.i18n',
	'django.core.context_processors.media',
	'context_processors.default_processors',
	)
	
ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
	os.path.join(PROJECT_DIR, 'templates')
)

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.admin',
	'debug_toolbar',
	'mediamanager',
	'tagging',
	'livesettings',
	'projects',
)

MEDIA_THUMBNAIL_SIZES = 150, 150