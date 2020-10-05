import pytest
from django.urls import reverse_lazy

pytestmark = pytest.mark.django_db


def test_urls_mynewapp_index():
    assert reverse_lazy("mynewapp:index") == "/mynewapp/"


def test_urls_mynewapp_mynewappmodel_list():
    assert reverse_lazy("mynewapp:mynewappmodels_list") == "/mynewapp/mynewappmodels/"
