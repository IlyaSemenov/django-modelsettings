import django.conf

from .settings import settings

django.conf.settings.db = settings

default_app_config = 'dbsettings.apps.SettingsConfig'
