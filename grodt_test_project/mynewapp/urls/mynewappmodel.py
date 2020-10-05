from django.urls import path

from .. import views

urlpatterns_mynewappmodel = [
    path('mynewappmodels/', views.MyNewAppModelListView.as_view(), name="mynewappmodels_list"),

    path('mynewappmodel/new/', views.MyNewAppModelCreateView.as_view(), name="mynewappmodel_create"),
    path('mynewappmodel/<uuid:uuidpk>/edit/', views.MyNewAppModelUpdateView.as_view(), name="mynewappmodel_edit"),
    path('mynewappmodel/<uuid:uuidpk>/delete/', views.MyNewAppModelDeleteView.as_view(), name="mynewappmodel_delete"),
    path('mynewappmodel/<uuid:uuidpk>/', views.MyNewAppModelDetailView.as_view(), name="mynewappmodel_detail"),
]
