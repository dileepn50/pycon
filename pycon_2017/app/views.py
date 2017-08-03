from django import http 
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.db import IntegrityError

from rest_framework import permissions  
from rest_framework.views import APIView
from rest_framework.response import Response

import json

from app import forms as app_forms 
from app import models as app_models  
from app import serializers as app_serializers   


class ViewProfile(APIView):
    def get(self, request):
        try:
            user = User.objects.get(username=request.user)
        except User.DoesNotExist:
            raise http.Http404('user does not exist')
        serializer = app_serializers.UserSerializer(user, many=False)
        return Response(serializer.data)


class EditProfile(TemplateView):
    def get(self, request):
        user = User.objects.get(username=request.user)
        serializer = app_serializers.UserSerializer(user, many=False)
        return http.JsonResponse(serializer.data, safe=False)

    def post(self, request):
        serializer = app_serializers.UserSerializer(data=request.POST)
        user = User.objects.get(username=request.user)
        if serializer.is_valid():
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.save()
            args = {'user': request.user.first_name}
            return render(request, 'profile_updated.html', args)


class HomeView(TemplateView):
    template_name = 'create_request.html'
    def get(self, request):
        user_is_present = app_models.reg_conference.objects.filter(user=request.user)
        args = {'user': request.user }
        if user_is_present:
            return render(request, 'request_already_created.html', args)

        form = app_forms.HomeForm() 
        return render(request, self.template_name, { 'form': form })
    def post(self, request):
        reg_conf_serializer = app_serializers.RegConferenceSerializer(data=request.POST)
        if reg_conf_serializer.is_valid():
            try:
                reg_conf_serializer.save(user=request.user)
            except IntegrityError as exc:
                return render(request, 'request_already_registered.html')    
            return render(request, 'request_confirmation.html')

        else:
            errors = reg_conf_serializer.errors
            error = "Input's you given are not correct. Please give the correct input details" 
            '''
            args = {'form': form, 'error': error}
            return render(request, self.template_name, args)
            '''


class RegUserDetails(TemplateView):
    def get(self, request, username):
        user_object = User.objects.get(username=username)
        user_reg_details = app_models.reg_conference.objects.get(user=user_object.id)
        serializer = app_serializers.RegConferenceSerializer(user_reg_details, many=False)
        response_data = serializer.data
        response_data['username'] = username
        return http.JsonResponse(response_data, safe=False)

    def post(self, request):
        username = request.POST['username']
        approve_status = request.POST['approve_status']
        user_object = User.objects.get(username=username)
        user_details = app_models.reg_conference.objects.get(user=user_object.id)
        user_details.approve_status = approve_status
        user_details.save()
        return redirect('/#!/app/admin') 


def request_details(request):
    args = {'user': request.user }
    try:
        user_details = app_models.reg_conference.objects.get(user=request.user)
    except app_models.reg_conference.DoesNotExist:
        return render(request, 'user_not_registered.html', args)
    else:
        serializer = app_serializers.RegConferenceSerializer(user_details)
        return http.JsonResponse(serializer.data, safe=False)


def get_states(request):
    try:
        state_li = app_models.state_list.objects.all()
    except app_models.state_list.DoesNotExist:
        raise http.Http404('unable to get state list')
    serializer = app_serializers.StateListSerializer(state_li, many=True)
    return http.JsonResponse(serializer.data, safe=False)


def admin_user(request):
   user = User.objects.get(username=request.user) 
   if not user.is_staff:
       args = { 'authorized': str(user.is_staff), 'admin': user.username }
       print(args)
       return http.JsonResponse(args)

   else:
       registered_user_list = [registered_user.user for registered_user in app_models.reg_conference.objects.all()]
       user_list = User.objects.all()
       print(user_list)
       #r_list = User.objects.filter(id__in=registered_user_list)
       serializer = app_serializers.RegUserSerializer(registered_user_list, many=True)
       state_names = [str(state) for state in app_models.state_list.objects.all()]
       print(state_names)
       args = {'authorized': str(user.is_staff), 'admin': str(request.user), 'user_list': serializer.data, 'state_list': state_names }
       return http.JsonResponse(args, safe=False)


def add_state(request):
    state = request.POST['name']
    serializer = app_serializers.StateListSerializer(data=request.POST)
    if serializer.is_valid():
        state_object = state_list(name=state)
        state_object.save()

    return redirect('/#!/app/admin')
        

def base(request):
    args = {'user': request.user}
    return render(request, 'base.html', args)


def register(request):
    if request.method == 'POST':
        form = app_forms.RegistrationForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('app/login_page') 

    else:
        form = app_forms.RegistrationForm()
        print(form)
        return render(request, 'reg_form.html', {'form': form})


def request_status(request):
    user_object = User.objects.get(username=request.user)
    try:
        reg_user_object = app_models.reg_conference.objects.get(user = user_object)
    except app_models.reg_conference.DoesNotExist:        
        args = {'username': str(request.user), 'not_registered': 'True'}
        return http.JsonResponse(args, safe=False)
    approve_status_details = {'c': 'cancelled', 'a': 'approved', 'w': 'weightinglist', 'y': 'yet to check'}
    args = {'username': str(request.user), 'status': approve_status_details[reg_user_object.approve_status], 'not_registered': 'False'}
    return http.JsonResponse(args, safe=False)


@login_required
def change_password(request):

    if request.method == 'POST':
        form = PasswordChangeForm(data = request.POST, user = request.user)
        if form.is_valid():
            form.save()
            return redirect('app/view_profile')

    else:
        form = PasswordChangeForm(user = request.user)
        args = {'form': form}
        return render(request, 'change_password.html', args)



