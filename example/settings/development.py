from defaults import *

DEBUG = True

TEMPLATE_DEBUG = True

INTERNAL_IPS = ('127.0.0.1', )

# DJANGO-PDB
INSTALLED_APPS += ('django_pdb', )
MIDDLEWARE_CLASSES += ('django_pdb.middleware.PdbMiddleware', )

# DJANGO DEBUG TOOLBAR
MIDDLEWARE_CLASSES = ('debug_toolbar.middleware.DebugToolbarMiddleware', ) + MIDDLEWARE_CLASSES
INSTALLED_APPS += (
    'django.contrib.admin',
    'debug_toolbar',
)
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}
