from django.urls import path

from .views import AboutPageView, HomePageView, usersettings

app_name = "pages"

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('usersettings/', usersettings, name='usersettings'),
]
