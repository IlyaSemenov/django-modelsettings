from django.db import models

from dbsettings.models import AppSettings


class Settings(AppSettings):
    test_char = models.CharField(max_length=25, default="foo")
    test_bool_true = models.BooleanField(default=True)
    test_bool_false = models.BooleanField(default=False)
