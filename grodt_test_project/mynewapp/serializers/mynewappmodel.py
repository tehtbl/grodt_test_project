from core import constants as core_const
from rest_framework import serializers

from ..models import MyNewAppModel


class MyNewAppModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyNewAppModel
        exclude = core_const.LIST_MODEL_FIELD_EXCLUDES

    def validate_name(self, value):
        """Check name constraints."""
        value = value.lower()
        return value

    def validate(self, data):
        return data

    def create(self, validated_data):
        """Set permissions."""
        mynewappmodel = MyNewAppModel(**validated_data)
        creator = self.context["request"].user

        mynewappmodel.save(creator=creator)

        return mynewappmodel
