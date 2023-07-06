from rest_framework import serializers
from users.models import (UserBase)
from core.utils.serializers import Base64ImageField


class RegisterUserBaseSerializer(serializers.ModelSerializer):
    profile_image = Base64ImageField(required=False)

    class Meta:
        model = UserBase
        fields = ('email', 'password', 'first_name', 'last_name', 'contact',
                  'profile_image')

        extra_kwargs = {
            'is_verified': {
                'read_only': True
            },
            'last_login': {
                'read_only': True
            },
            'is_staff': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserBase
        fields = ('email', 'password', 'first_name', 'last_name', 'contact',
                  'profile_image', 'is_verified', 'last_login', 'is_staff',
                  'id')

        extra_kwargs = {
            'id': {
                'read_only': True
            },
            'email': {
                'write_only': True
            },
            'is_verified': {
                'read_only': True
            },
            'last_login': {
                'read_only': True
            },
            'is_staff': {
                'read_only': True
            },
            'password': {
                'write_only': True
            }
        }

    def update(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
