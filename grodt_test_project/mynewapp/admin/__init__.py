from django.contrib import admin

from ..models import MyNewAppModel
from .mynewappmodel import MyNewAppModelAdmin

admin.site.register(MyNewAppModel, MyNewAppModelAdmin)
