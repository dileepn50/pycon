from django.contrib.auth.models import User
from .models import state_list, reg_conference
from rest_framework import serializers



class state_listSerializer(serializers.ModelSerializer):
    class Meta:
        model = state_list
        fields = ('name',)



class reg_conferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = reg_conference
        #fields = ('first_name', 'last_name', 'phone_number', 'email', 'company', 'address', 'state', 'user')
        fields = ('first_name', 'last_name', 'email', 'company', 'address', 'state', 'phone_number', 'approve_status')



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'id')


class reg_userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)
