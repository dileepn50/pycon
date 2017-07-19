from django.contrib.auth.models import User
from .models import state_list, reg_conference
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class state_listSerializer(serializers.ModelSerializer):
    class Meta:
        model = state_list
        fields = ('name',)



class reg_conferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = reg_conference
        fields = ('first_name', 'last_name', 'phone_number', 'email', 'company', 'address', 'state' )
