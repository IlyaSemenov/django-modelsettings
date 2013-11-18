from .proxy import settings


class InvalidateSettingsMiddleware(object):
	def process_request(self, request):
		settings.invalidate()
