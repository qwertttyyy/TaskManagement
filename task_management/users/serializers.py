from rest_framework import serializers
from rest_framework import exceptions as rest_framework_exceptions
from django.core import exceptions as django_exceptions

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'email', 'password']

    def create(self, validated_data):
        try:
            user = CustomUser.objects.create_user(**validated_data)
        except django_exceptions.ValidationError as error:
            raise rest_framework_exceptions.ValidationError(error.messages)
        return user
