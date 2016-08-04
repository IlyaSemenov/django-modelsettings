from django.contrib import admin
from django.core.urlresolvers import reverse, NoReverseMatch
from django.shortcuts import redirect

from .models import Root


@admin.register(Root)
class SettingsAdmin(admin.ModelAdmin):
	def has_add_permission(self, request):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

	def has_change_permission(self, request, obj=None):
		try:
			reverse('dbsettings')
		except NoReverseMatch:
			return False
		else:
			return True

	def changelist_view(self, request, extra_context=None):
		return redirect('dbsettings')

	def change_view(self, request, object_id, form_url='', extra_context=None):
		return redirect('dbsettings')
