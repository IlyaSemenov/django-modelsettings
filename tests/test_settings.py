import pytest
from django.test import TestCase
from dbsettings import settings


@pytest.mark.django_db
def test_simple():
    assert settings.test1.test_char == "foo"


@pytest.mark.django_db
def test_bool_true():
    assert settings.test1.test_bool_true == True


@pytest.mark.django_db
def test_bool_false():
    assert settings.test1.test_bool_false == False
