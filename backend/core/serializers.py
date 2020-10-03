from allauth.account.adapter import get_adapter
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from . import models

import datetime



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('email', 'username', 'password', 'mobile', 'profile_pic', 'first_name', 'last_name')


class CustomRegisterSerializer(RegisterSerializer):
    mobile = serializers.CharField(allow_blank = True, allow_null=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField(allow_blank = True, allow_null=True)
    email = serializers.EmailField(allow_blank = True, allow_null=True)

    class Meta:
        model = models.User
        fields = ('email', 'username', 'password', 'mobile', 'first_name', 'last_name')

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
            'mobile': self.validated_data.get('mobile', ''),

        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.mobile = self.cleaned_data.get('mobile')
        user.save()
        adapter.save_user(request, user, self)
        return user


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Token
        fields = ('key', 'user')

