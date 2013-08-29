import proxy


def settings(request):
	return {'settings': proxy.settings}
