from django.db import models
from django.db.models.base import ModelBase


registered_settings = {}


class SettingsDefiningClass(ModelBase):
	def __new__(cls, name, bases, attrs):
		new_class = super(SettingsDefiningClass, cls).__new__(cls, name, bases, attrs)
		if not new_class._meta.abstract:
			meta = new_class._meta
			if not meta.app_label in registered_settings:
				registered_settings[meta.app_label] = {}
			registered_settings[meta.app_label][meta.module_name] = new_class
		return new_class


class Root(models.Model):
	pass


class Settings(models.Model):
	__metaclass__ = SettingsDefiningClass
	root = models.OneToOneField(Root, primary_key=True, related_name='%(app_label)s_%(class)s', editable=False)

	class Meta:
		abstract = True
