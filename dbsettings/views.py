from django.conf import settings
from django.contrib import messages
from django.contrib.admin import ModelAdmin
from django.contrib.admin.helpers import Fieldset
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, render

from .models import get_settings_models


class FakeOpts(object):
	def get_ordered_objects(self):
		return None


@user_passes_test(lambda user: user.is_staff)
def edit_settings(request):
	forms = []
	fieldsets = []

	for app, model in get_settings_models():
		# TODO: check permissions for specific models
		instance = getattr(settings.db, model._get_settings_object_name())
		model_admin = ModelAdmin(model, None)  # TODO: allow to override
		form_class = model_admin.get_form(request, instance)
		form = form_class(
			prefix=model._get_settings_object_name(),
			instance=instance,
			data=request.POST or None,
			files=request.FILES or None,
		)
		fieldset = Fieldset(
			form,
			name=app.verbose_name if model._meta.model_name == 'settings' else '{}: {}'.format(app.verbose_name, model._meta.verbose_name.capitalize()),
			fields=list(form.fields.keys()) + list(model_admin.readonly_fields),
			readonly_fields=model_admin.readonly_fields,
		)
		forms.append(form)
		fieldsets.append(fieldset)

	if all([form.is_valid() for form in forms]):  # need to use list (not generator!) to validate all forms
		for form in forms:
			form.save()
		messages.info(request, "Settings saved.")
		return redirect(request.get_full_path())

	context = {
		'app_name': "Settings",
		'forms': forms,
		'fieldsets': fieldsets,
		'opts': FakeOpts(),
		'change': True,
		'is_popup': False,
		'save_as': False,
		'has_add_permission': False,
		'has_delete_permission': False,
		'has_change_permission': True,
		# 'media':  # TODO: merge model_admin media
	}
	return render(request, 'dbsettings/settings.html', context)
