from django.http import HttpResponse, JsonResponse, HttpResponsePermanentRedirect
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate 
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView

import json

from app.forms import RegistrationForm, EditProfileForm, HomeForm
from app.models import reg_conference, state_list 
from permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.http import Http404

from django.db import IntegrityError
from .serializers import UserSerializer, state_listSerializer, reg_conferenceSerializer, reg_userSerializer 
from rest_framework.response import Response

from django.contrib.auth.models import User
def base(request):
        args = {'user': request.user}
        return render(request, 'base.html', args)


def login_redirect(request):
    return redirect('app/login_page')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('app/login_page') 
    else:
        form = RegistrationForm()
        print(form)
        return render(request, 'reg_form.html', {'form': form})


def request_status(request):
    user_object = User.objects.get(username=request.user)
    try:
        reg_user_object = reg_conference.objects.get(user = user_object)
    except reg_conference.DoesNotExist:        
        args = {'username': str(request.user), 'not_registered': 'True'}
        return JsonResponse(args, safe=False)
    approve_status_details = {'c': 'cancelled', 'a': 'approved', 'w': 'weightinglist', 'y': 'yet to check'}
    args = {'username': str(request.user), 'status': approve_status_details[reg_user_object.approve_status], 'not_registered': 'False'}
    return JsonResponse(args, safe=False)

#@login_required
class view_profile(APIView):
    #form = EditProfileForm(request.POST, instance = request.user)
    def get(self, request):
        try:
            user = User.objects.get(username=request.user)
        except User.DoesNotExist:
            raise Http404('user does not exist')
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    def post(self, request):
        pass

#@login_required
class edit_profile(TemplateView):
    #permission_classes = (IsAdminOrReadOnly, )
      
    def get(self, request):
        user = User.objects.get(username=request.user)
        serializer = UserSerializer(user, many=False)
        return JsonResponse(serializer.data, safe=False)
    def post(self, request):
        serializer = UserSerializer(data=request.POST)
        user = User.objects.get(username=request.user)
        if serializer.is_valid():
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.save()
            args = {'user': request.user.first_name}
            return render(request, 'profile_updated.html', args)

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

class HomeView(TemplateView):
    permission_classes = (IsAdminOrReadOnly, IsAuthenticated)
    template_name = 'create_request.html'
    def get(self, request):
        user_is_present = reg_conference.objects.filter(user=request.user)
        args = {'user': request.user }
        if user_is_present:
            return render(request, 'request_already_created.html', args)
        form = HomeForm() 

        return render(request, self.template_name, { 'form': form })
    def post(self, request):
        reg_conf_serializer = reg_conferenceSerializer(data=request.POST)
        if reg_conf_serializer.is_valid():
            try:
                reg_conf_serializer.save(user=request.user)
            except IntegrityError as exc:
                return render(request, 'request_already_registered.html')    
            return render(request, 'request_confirmation.html')
        else:
            print(reg_conf_serializer)
            errors = reg_conf_serializer.errors
            print(errors)
            error = "Input's you given are not correct. Please give the correct input details" 
            '''
            args = {'form': form, 'error': error}
            return render(request, self.template_name, args)
            '''


def request_details(request):
    args = {'user': request.user }
    try:
        user_details = reg_conference.objects.get(user=request.user)
    except reg_conference.DoesNotExist:
        return render(request, 'user_not_registered.html', args)
    else:
        serializer = reg_conferenceSerializer(user_details)
        return JsonResponse(serializer.data, safe=False)

def get_states(request):
    try:
        state_li = state_list.objects.all()
    except state_list.DoesNotExist:
        raise Http404('unable to get state list')
    serializer = state_listSerializer(state_li, many=True)
    return JsonResponse(serializer.data, safe=False)

def admin_user(request):
   user = User.objects.get(username=request.user) 
   if not user.is_staff:
       args = { 'authorized': str(user.is_staff), 'admin': user.username }
       print(args)
       return JsonResponse(args)
   else:
       registered_user_list = [registered_user.user for registered_user in reg_conference.objects.all()]
       user_list = User.objects.all()
       print(user_list)
       #r_list = User.objects.filter(id__in=registered_user_list)
       serializer = reg_userSerializer(registered_user_list, many=True)
       state_names = [str(state) for state in state_list.objects.all()]
       print(state_names)
       args = {'authorized': str(user.is_staff), 'admin': str(request.user), 'user_list': serializer.data, 'state_list': state_names }
       return JsonResponse(args, safe=False)

        
class reg_user_details(TemplateView):
    def get(self, request, username):
        user_object = User.objects.get(username=username)
        user_reg_details = reg_conference.objects.get(user=user_object.id)
        serializer = reg_conferenceSerializer(user_reg_details, many=False)
        response_data = serializer.data
        response_data['username'] = username
        print(response_data)
        return JsonResponse(response_data, safe=False)
    def post(self, request):
        username = request.POST['username']
        approve_status = request.POST['approve_status']
        user_object = User.objects.get(username=username)
        user_details = reg_conference.objects.get(user=user_object.id)
        user_details.approve_status = approve_status
        user_details.save()
        return redirect('/#!/app/admin') 
        

def add_state(request):
    state = request.POST['name']
    print('-' * 20)
    print(state)
    print('-' * 20)
    serializer = state_listSerializer(data=request.POST)
    if serializer.is_valid():
        state_object = state_list(name=state)
        state_object.save()
        print(state + ' is added to state list')
    return redirect('/#!/app/admin')
        










