from dbsettings import settings as settings_dbsettings


def settings(request):
    """returns all settings in a dict to provide templates with setting access."""
    return {"settings": settings_dbsettings}
