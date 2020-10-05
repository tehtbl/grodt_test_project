from ckeditor_uploader import views as cku_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from django.views.i18n import JavaScriptCatalog
from rest_framework.renderers import JSONOpenAPIRenderer
from rest_framework.schemas import get_schema_view

urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    path("users/", include("django.contrib.auth.urls")),
    path("accounts/", include("allauth.urls")),

    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
    path("ckeditor/upload/", login_required(cku_views.upload), name="ckeditor_upload"),
    path("ckeditor/browse/", login_required(cku_views.browse), name="ckeditor_browse"),

    path("", include("grodt_test_project.pages.urls")),
    path("mynewapp/", include("grodt_test_project.mynewapp.urls")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# API urls
schema_view = get_schema_view(
    title="GRODT Test Project API",
    version="v0.1.0",
    public=False,
    renderer_classes=[JSONOpenAPIRenderer],
)

urlpatterns += [
    path("docs/openapi.json", schema_view, name="openapi_schema"),
    path("docs/api/", login_required(TemplateView.as_view(template_name="swagger-ui.html")), name="docs-index"),

    # DRF auth token
    # path("auth-token/", obtain_auth_token),

    path(settings.MY_API_PREFIX + "mynewapp/", include("grodt_test_project.mynewapp.urls_api")),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]

    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
