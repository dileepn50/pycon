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
from .serializers import UserSerializer, state_listSerializer, reg_conferenceSerializer 
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
        print(serializer.errors)

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
            error = reg_conf_serializer.errors
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
   if user.is_staff:
       args = { 'authorized': False, 'username': user.username }
       return JsonResponse(args)


