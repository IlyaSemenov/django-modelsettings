def collect_settings():
	# Relative models import here allows the module to be imported during Django app init phase
	from .models import Root, get_settings_models

	selectors = []
	select_related = []
	for app, model in get_settings_models():
		field = '{}_{}'.format(model._meta.app_label, model._meta.model_name)
		select_related.append(field)
		selectors.append((app, model, field))

	qs = Root.objects.select_related(*select_related)
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
