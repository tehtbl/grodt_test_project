from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.decorators import user_passes_test

from .forms import MyUserChangeForm, MyUserCreationForm
from .models import MyUser, ObjectAccess


class CustomUserAdmin(UserAdmin):
    add_form = MyUserCreationForm
    form = MyUserChangeForm
    model = MyUser
    list_display = ['username', ]


admin.site.register(MyUser, CustomUserAdmin)
admin.site.register(ObjectAccess)

# admin.site.login = login_required(admin.site.login)
admin.site.login = user_passes_test(lambda u: u.is_superuser)(admin.site.login)
