from rest_framework import routers

from .. import api

router = routers.SimpleRouter()
router.register(r"mynewappmodels", api.MyNewAppModelViewSet, basename="mynewappmodel")

urlpatterns_mynewappmodel = router.urls
