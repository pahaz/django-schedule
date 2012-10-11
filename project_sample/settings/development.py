from defaults import *

DEBUG = True

INTERNAL_IPS = ('127.0.0.1', )

# DJANGO DEBUG TOOLBAR
MIDDLEWARE_CLASSES = ('debug_toolbar.middleware.DebugToolbarMiddleware', ) + MIDDLEWARE_CLASSES
INSTALLED_APPS += (
    'django.contrib.admin',
    'debug_toolbar',
)
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}
