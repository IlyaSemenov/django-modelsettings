from .proxy import settings as settings_object


def settings(request):
	return {'settings': settings_object}
