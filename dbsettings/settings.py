import django.conf
from django.core.signals import request_finished
from django.dispatch import receiver

from .collector import CollectedSettings

settings = CollectedSettings()

settings.django = django.conf.settings
django.conf.settings.db = settings


@receiver(request_finished)
def on_request_finished(sender, **kwargs):
	settings.invalidate()
