django-modelsettings
====================

This Django application allows to create user-adjustable application settings which are stored in database models. 

Please check the other alternatives at [https://www.djangopackages.com/grids/g/live-setting/](https://www.djangopackages.com/grids/g/live-setting/). This project started because I tried them all and I was not really happy with any of them.

Key points
----------

1. The settings are stored in the database, in normalized tables with proper field types and constraints. In particular, it is possible to have a setting which is a ForeignKey to another model (think of "Default account"), and it will properly validate and/or update when the corresponding model is deleted.

2. The settings are described using standard `django.db.models.Field` classes (like `EmailField` or `SmallPositiveIntegerField`), with all the bells and whistles (like validators). There is no parallel hierarchy of classes for different types of data. Defining a group of settings is nothing different from defining a typical `Model` class, it's only that this model will be a singleton and there will be the additional easy way to access its data.

3. Each application may have any number of setting groups, however there is no fancy and complex syntax for that. The developer may simply add more `Settings` classes if he decides so.

4. The settings are lazy and effective. The database is not hit until the settings are actually accessed. Then it takes exactly one SQL query to fetch all the settings (it uses `select_related` internally), which may be further be optimized by using Django caching framework. The system behaves correctly when there is no data in the database (if the settings have never been saved yet, or have been saved partly).

5. Programmatically, all settings from all application are nicely accessible via a single object.

5. The application provides the administrative UI which takes one line of code to enable (it is monkey-patchey though).

Usage
-----

Register the application in `settings.py`:

```python
INSTALLED_APPS =
	...
	'dbsettings',
	...
```

Create a `Settings` class in your application's `models.py`:

```python
import dbsettings

class Settings(dbsettings.Settings):
	contact_email = models.EmailField(default="info@localhost")
	update_interval = models.PositiveIntegerField(null=True, default=10, help_text="Update interval in seconds")
	facebook_app_id = models.CharField("Facebook App ID", max_length=32, blank=True)
```

Create the corresponding database tables: `./manage.py syncdb`.
If you use [South](http://south.aeracode.org/) database migration tool, also run
`./manage.py schemamigration blog --auto && ./manage.py migrate blog`, where `blog` is your application's name.

In your business logic code, use settings like that:

```python
from dbsettings import settings

print settings.blog.contact_email # where blog is your application's name

settings.blog.update_interval = 60
settings.blog.save()
```

Enable the admin area by adding this before you do the autodiscover (normally in `urls.py`):

```python
import dbsettings

dbsettings.add_to_admin(admin.site)
admin.autodiscover()
```

The admin area will be accessible at [http://localhost:8000/admin/settings/](http://localhost:8000/admin/settings/) (or under other prefix which you chose for `admin.site.urls`). To add a link to Settings page to the admin site header, create `admin/base_site.html` template:

```html
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
```

### Production (or multi-threaded development)

In production environment you will need to invalidate settings on time (read more on caching and invalidation options in [Caching](#caching) below):

```python
MIDDLEWARE_CLASSES =
	...
	'dbsettings.middleware.InvalidateSettingsMiddleware',
	...
```

Advanced
--------

### Several groups of settings per application

Sometimes it is convenient to split settings into several groups within one application. This may be achieved like that:

```python
import dbsettings

class FooSettings(dbsettings.Settings):
	option1 = models.IntegerField()

class BarSettings(dbsettings.Settings):
	option2 = models.IntegerField()

class Settings(dbsettings.Settings): # not required
	option3 = models.IntegerField()

...

from dbsettings import settings

print settings.blog_foosettings.option1
print settings.blog_barsettings.option2
print settings.blog.option3
```

Yes, I realize that `settings.blog.foo.option1` would make it cleaner, and I may try to implement this in future.

### Customizing the admin area

It is possible to customize the admin area forms which are used to edit the settings, for instance:

```python
from django import forms
from django.contrib import admin
from blog.models import Settings

class SettingsForm(forms.ModelForm):
    class Meta:
      model = Settings
        
    def clean(self):
        # your logic goes here

class SettingsAdmin(admin.ModelAdmin):
    form = SettingsForm
	raw_id_fields = 'default_account',
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        # your logic goes here

admin.site.register_settings(Settings, SettingsAdmin)
```
This is not required to explicitly register all Settings classes, it is only needed if you need to override the default behavior.

### Accessing from templates

To access settings from templates, you need to pass the `settings` object to the render context. Of course there are multiple ways to do that, but there is a handy template context processor included.

```python
TEMPLATE_CONTEXT_PROCESSORS =
    ...
    'dbsettings.context_processors.settings',
    ...
```

Then you access settings like this:

```html
<p>You may reach us at {{ settings.blog.contact_email }}</p>
```

### Caching

There are two tiers of caching data in dbsettings:

1. By default settings are cached in dbsettings.settings (a Python object). When running in multi-process environment (such as nginx+UWSGI) this needs to be invalidated from time to time to ensure that all worker processes catch changes made by the other processes. Typically, you would do that on each HTTP request by including the provided middleware:
	```python
	MIDDLEWARE_CLASSES =
		...
		'dbsettings.middleware.InvalidateSettingsMiddleware',
		...
	```

2. **(Not currently implemented)** Additionally, settings may be cached using [Django caching framework](https://docs.djangoproject.com/en/dev/topics/cache/). If this is enabled, when settings are about to be read from the database (either on first access, or after invalidation), an attempt will be made to retrieve them from Django cache.
```python
DBSETTINGS_CACHE_ALIAS = 'default' # Django cache alias to use
```

### Naming clash with django.conf.settings

Unfortunately, `dbsettings.settings` clashes with `django.conf.settings` so you can't import both into the same namespace. In this case, use one of the provided shortcuts to access the counterpart object:

```python
from django.conf import settings

print settings.SECRET_KEY
print settings.db.blog.contact_email
```

or:

```python
from dbsettings import settings

print settings.blog.contact_email
print settings.django.SECRET_KEY
```
