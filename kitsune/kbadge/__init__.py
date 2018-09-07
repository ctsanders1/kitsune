from django.conf import settings
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule

BADGER_BADGE_PAGE_SIZE = 12
BADGER_MAX_RECENT = 15
BADGER_TEMPLATE_BASE = 'badger'


def autodiscover():
    """
    Auto-discover INSTALLED_APPS badges.py modules and fail silently when
    not present.
    """
    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        try:
            badges_mod = import_module('%s.badges' % app)
            if hasattr(badges_mod, 'register_signals'):
                badges_mod.register_signals()
        except ImportError:
            if module_has_submodule(mod, 'badges'):
                raise
