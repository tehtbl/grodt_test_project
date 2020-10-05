from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import MyUser


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = MyUser
        fields = ('username',)


class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = MyUser
        fields = ('username',)
