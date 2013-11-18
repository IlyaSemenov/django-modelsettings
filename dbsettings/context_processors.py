from .proxy import settings as proxy


def settings(request):
	return {'settings': proxy}
