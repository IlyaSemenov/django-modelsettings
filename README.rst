django-modelsettings
====================

This Django application allows to define Django application settings with Django ORM models and edit them in the admin area.

Please check the other alternatives at https://www.djangopackages.com/grids/g/live-setting/.
This project started because I tried them all and I was not really happy with any of them.


Key points
----------

1. The settings are stored in the database, in normalized tables with proper field types and constraints. In particular, it is possible to have a setting which is a ForeignKey to another model (e.g. "Default account"), and it will properly validate and/or update when the corresponding model is deleted.

2. The settings are described using standard Django ORM classes (like ``EmailField`` or ``SmallPositiveIntegerField``) with all the bells and whistles (e.g. validators). There is no parallel hierarchy of classes for different types of data.

3. Each application may have any number of settings groups, however there is no fancy and complex syntax for that. The developer may simply add more ``Settings`` classes if he decides so.

4. The settings are lazy and effective. The database is not hit until the settings are actually accessed, and then it takes exactly one SQL query to fetch all settings for all apps.

5. The system behaves correctly when there is no corresponding data in the database (if the settings have never been saved yet, or have been saved partly).

6. Programmatically, all settings from all application are accessible via a single object.

7. There is a page for Django Admin.


Requirements
============

The latest version supports Django 1.7-1.9.

django-modelsettings 0.1.x had a different, more hackish API and supported Django 1.4-1.8.


Installation
============

::

	pip install django-modelsettings


Usage
=====

Add ``dbsettings`` to ``INSTALLED_APPS``:

.. code:: python

	# settings.py

	INSTALLED_APPS = [
		...
		'dbsettings',
	]


Add ``Settings`` class in your application:

.. code:: python

	# blog/models.py

	from dbsettings.models import BaseSettings

	class Settings(BaseSettings):
		contact_email = models.EmailField(default="info@localhost")
		update_interval = models.PositiveIntegerField(null=True, default=10, help_text="Update interval in seconds")
		facebook_app_id = models.CharField("Facebook App ID", max_length=32, blank=True)


Create the corresponding database tables:

.. code:: bash

	./manage.py makemigrations && ./manage.py migrate


In your business logic code, access settings directly:

.. code:: python

	from dbsettings import settings

	print(settings.blog.contact_email)

	settings.blog.update_interval = 60
	settings.blog.save()


...or via ``django.conf.settings.db`` shortcut:

.. code:: python

	from django.conf import settings

	print(settings.db.blog.contact_email)

	settings.db.blog.update_interval = 60
	settings.db.blog.save()


Admin area
----------

Enable the admin area by adding a route:

.. code:: python

	# urls.py

	import dbsettings.urls

	urlpatterns = [
       	url(r'^admin/settings/', include(dbsettings.urls)),
		...
	]


To add a link to Settings page to the admin site header, add ``admin/base_site.html`` template to your project:

.. code:: html

	{% extends "admin/base.html" %}
	{% load i18n %}

	{% block branding %}
		<h1 id="site-name">
			<a href="{% url 'admin:index' %}">{% trans "Administration" %}</a> |
			{% if user.is_superuser %}
				<a href="{% url 'admin:settings' %}">{% trans "Settings" %}</a> |
			{% endif %}
			<a href="/">{% trans "Back to site" %}</a>
		</h1>
	{% endblock %}


Several groups of settings per application
------------------------------------------

It is possible to split settings into several groups within one application.

.. code:: python

	from dbsettings.models import BaseSettings

	class Settings(BaseSettings):
		option1 = models.IntegerField()

	class FooSettings(BaseSettings):
		option2 = models.IntegerField()

	class BarSettings(BaseSettings):
		option3 = models.IntegerField()

	...

	from dbsettings import settings

	print(settings.blog.option1)
	print(settings.blog_foosettings.option2)
	print(settings.blog_barsettings.option3)
