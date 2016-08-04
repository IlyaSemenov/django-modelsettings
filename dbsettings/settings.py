import django.conf
from django.core.signals import request_finished
from django.dispatch import receiver


def collect_settings():
	# Relative models import here allows the module to be imported during Django app init phase
	from .models import Settings, get_settings_models

	selectors = []
	select_related = []
	for app, model in get_settings_models():
		field = '{}_{}'.format(model._meta.app_label, model._meta.model_name)
		select_related.append(field)
		selectors.append((app, model, field))

	qs = Settings.objects.select_related(*select_related)
	root = qs.first()
	if not root:
		root = qs.get_or_create()[0]

	settings = {}
	for app, model, root_field in selectors:
		try:
			v = getattr(root, root_field)
		except model.DoesNotExist:
			v = model(root=root)

		settings_field = model._get_settings_object_name()
		settings[settings_field] = v

	return settings


class CollectedSettings(object):
	def __init__(self):
		self.settings = None

	def __getattr__(self, item):
		if self.settings is None:
			self.settings = collect_settings()
		return self.settings[item]

	def invalidate(self):
		self.settings = None


settings = CollectedSettings()

settings.django = django.conf.settings
django.conf.settings.db = settings
print("db", django.conf.settings.db)

@receiver(request_finished)
def on_request_finished(sender, **kwargs):
	settings.invalidate()
