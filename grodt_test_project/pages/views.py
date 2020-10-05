from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView
from users.models import MyUser

from .forms import MyUserForm


class HomePageView(TemplateView):
    template_name = 'pages/home.html'


class AboutPageView(TemplateView):
    template_name = 'pages/about.html'


@login_required
def usersettings(request, tplname="pages/form.html"):
    user_obj = get_object_or_404(MyUser, username__exact=request.user.username)

    formset = MyUserForm(instance=user_obj)
    if request.method == "POST":
        formset = MyUserForm(request.POST, instance=user_obj)

        if formset.is_valid():
            formset.save()

    ctx = {
        "form": formset
    }
    return render(request, tplname, ctx)
