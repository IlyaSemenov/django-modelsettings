from django.db import models
from django.db.models.base import ModelBase


registered_settings = {}


def with_metaclass(meta, base=object):
	return meta("NewBase", (base,), {})


class SettingsDefiningClass(ModelBase):
	def __new__(mcs, name, bases, attrs):
		module_name = attrs.get('__module__', __name__)
		if name == 'NewBase' and not attrs:
			attrs['__module__'] = module_name
			attrs['Meta'] = type('Meta', (object, ), {'abstract': True})
		new_class = super(SettingsDefiningClass, mcs).__new__(mcs, name, bases, attrs)

		meta = getattr(new_class, '_meta')
		abstract = getattr(meta, 'abstract', False)
		app_label = getattr(meta, 'app_label', module_name.split('.')[-2:][0])

		if not abstract:
			if not app_label in registered_settings:
				registered_settings[app_label] = {}
			registered_settings[app_label][name.lower()] = new_class

		return new_class


class Root(models.Model):
	pass


class Settings(with_metaclass(SettingsDefiningClass, models.Model)):
	root = models.OneToOneField(Root, primary_key=True, related_name='%(app_label)s_%(class)s', editable=False)

	class Meta:
		abstract = True
