from django.urls import path

from .. import views
from .mynewappmodel import urlpatterns_mynewappmodel

app_name = "mynewapp"

urlpatterns = [
    path('', views.index, name="index"),
]

urlpatterns += urlpatterns_mynewappmodel
