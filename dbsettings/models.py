from django.apps import apps
from django.db import models


class Root(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = 'settings'


class AppSettings(models.Model):
	root = models.OneToOneField(Root, primary_key=True, related_name='%(app_label)s_%(class)s', editable=False)
	settings_object_name = None

	class Meta:
		abstract = True

	@classmethod
	def _get_settings_object_name(cls):
		# app.Settings => app
		# app.MySettings => app_mysettings
		return cls.settings_object_name or (cls._meta.app_label if cls._meta.model_name == 'settings' else '{}_{}'.format(cls._meta.app_label, cls._meta.model_name))


def get_settings_models():
	for app in apps.get_app_configs():
		for model in app.get_models():
			if issubclass(model, AppSettings) and not model._meta.abstract:
				yield app, model
