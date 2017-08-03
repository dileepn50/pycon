from django.contrib.auth.models import User
from rest_framework import serializers

from app import models as app_models 


class StateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = app_models.state_list
        fields = ('name',)


class RegConferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = app_models.reg_conference
        #fields = ('first_name', 'last_name', 'phone_number', 'email', 'company', 'address', 'state', 'user')
        fields = ('first_name', 'last_name', 'email', 'company', 'address', 'state', 'phone_number', 'approve_status')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'id')


class RegUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)
