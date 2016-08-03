from django.conf.urls import url

from . import views


urlpatterns = [
	url(r'^$', views.edit_settings, name='dbsettings'),
]
