from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse


@login_required
def index(request):
    return HttpResponseRedirect(reverse("mynewapp:mynewappmodels_list"))
