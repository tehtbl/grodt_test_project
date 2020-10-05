from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated

from ..models import MyNewAppModel
from ..serializers import MyNewAppModelSerializer


class MyNewAppModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, DjangoModelPermissions, ]
    serializer_class = MyNewAppModelSerializer

    def get_queryset(self):
        """Filter queryset based on current user."""
        return MyNewAppModel.objects.get_for_admin(self.request.user)

    def perform_destroy(self, instance):
        """Add custom args to delete call."""
        instance.delete(self.request.user)
