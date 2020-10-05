from django.contrib.auth import mixins as auth_mixins
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from ..forms import MyNewAppModelFormGeneral
from ..models import MyNewAppModel


class MyNewAppModelCreateView(auth_mixins.PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = MyNewAppModel
    form_class = MyNewAppModelFormGeneral
    permission_required = "mynewapp.add_mynewappmodel"
    template_name = "mynewapp/mynewappmodel/form.html"
    success_url = reverse_lazy("mynewapp:mynewappmodels_list")
    success_message = "%(name)s was created successfully"


class MyNewAppModelUpdateView(auth_mixins.PermissionRequiredMixin, UpdateView):
    model = MyNewAppModel
    form_class = MyNewAppModelFormGeneral
    permission_required = "mynewapp.edit_mynewappmodel"
    template_name = "mynewapp/mynewappmodel/form.html"
    success_url = reverse_lazy("mynewapp:mynewappmodels_list")
    pk_url_kwarg = 'uuidpk'


class MyNewAppModelDeleteView(auth_mixins.PermissionRequiredMixin, DeleteView):
    model = MyNewAppModel
    permission_required = "mynewapp.del_mynewappmodel"
    success_url = reverse_lazy("mynewapp:mynewappmodels_list")
    pk_url_kwarg = 'uuidpk'

    # Now, there's no ``confirmation is required'' anymore!
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class MyNewAppModelDetailView(auth_mixins.PermissionRequiredMixin, generic.DetailView):
    model = MyNewAppModel
    permission_required = "mynewapp.view_mynewappmodel"
    template_name = "mynewapp/mynewappmodel/detail.html"
    pk_url_kwarg = 'uuidpk'


class MyNewAppModelListView(auth_mixins.PermissionRequiredMixin, ListView):
    model = MyNewAppModel
    permission_required = "mynewapp.view_mynewappmodel"
    template_name = "mynewapp/mynewappmodel/list.html"
    context_object_name = "my_mynewappmodels"
