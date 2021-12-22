from django.test import TestCase
from dbsettings import settings


class SettingsTest(TestCase):
    def test_simple(self):
        self.assertEqual(settings.test1.test_char, "foo")

    def test_bool_true(self):
        self.assertEqual(settings.test1.test_bool_true, True)

    def test_bool_false(self):
        self.assertEqual(settings.test1.test_bool_false, False)
