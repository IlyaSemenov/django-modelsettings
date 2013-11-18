from django.forms.models import modelform_factory
from django.contrib import messages
from django.contrib.admin import ModelAdmin
from django.contrib.admin.sites import AlreadyRegistered
from django.contrib.admin.helpers import Fieldset
from django.core.urlresolvers import reverse
from django.shortcuts import Http404, redirect
from django.template.response import TemplateResponse
from .models import registered_settings
from .proxy import settings


class FakeOpts(object):
	def get_ordered_objects(self):
		return None


def add_to_admin(admin_site):
	class AdminSite(admin_site.__class__):
		def get_urls(self):
			from django.conf.urls import patterns, url, include
			urlpatterns = patterns('',
				url(r'^settings/$', self.admin_view(self.settings_index), name='settings'),
				url(r'^settings/(\w+)/$', self.admin_view(self.app_settings), name='app_settings')
			)
			return urlpatterns + super(AdminSite, self).get_urls()

		def settings_index(self, request):
			apps = []
			for app_name in sorted(registered_settings.keys()):
				app = {
					'name': app_name.title(),
					'url': reverse('admin:app_settings', args=[app_name], current_app=self.name)
				}
				apps.append(app)
			context = {'apps': apps}
			return TemplateResponse(request, 'admin/dbsettings/index.html', context, current_app=self.name)

		def app_settings(self, request, app_name):
			model_classes = registered_settings.get(app_name)
			if not model_classes:
				raise Http404
			forms = []
			fieldsets = []
			for model_name, model in model_classes.items():
				instance = getattr(settings, '%s_%s' % (app_name, model_name))
				model_admin = self.registered_settings.get(model)
				if not model_admin:
					model_admin = ModelAdmin(model, self)
				Form = model_admin.get_form(request, instance)
				form = Form(prefix=model_name, data=request.POST or None, instance=instance)
				forms.append(form)
				fieldsets.append(Fieldset(
					form,
					name = '%s %s' % (app_name.title(), model._meta.verbose_name),
					fields = list(form.fields.keys()) + list(model_admin.readonly_fields),
					readonly_fields = model_admin.readonly_fields,
				))
			if all([form.is_valid() for form in forms]): # list to make all of them evaluate
				for form in forms:
					form.save()
				messages.info(request, "%s settings have been saved." % app_name.title())
				if '_save' in request.POST:
					return redirect(reverse('admin:settings', current_app=self.name))
				return redirect(request.get_full_path())
			context = {
				'app_name': app_name.title(),
				'forms': forms,
				'fieldsets': fieldsets,
				'opts': FakeOpts(),
				'change': True,
				'is_popup': False,
				'save_as': False,
				'has_add_permission': False,
				'has_delete_permission': False,
				'has_change_permission': True,
				'media': model_admin.media,
			}
			return TemplateResponse(request, 'admin/dbsettings/app_settings.html', context, current_app=self.name)

		def register_settings(self, settings, settings_admin):
			if settings in self.registered_settings:
				raise AlreadyRegistered("The settings class %s.%s is already registered" % (settings.__module__, settings.__name__))
			self.registered_settings[settings] = settings_admin(settings, self)

	def init(self):
		self.registered_settings = {}

	admin_site.__class__ = AdminSite
	init(admin_site)
