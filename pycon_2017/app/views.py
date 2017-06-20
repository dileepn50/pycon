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
from app.models import reg_conference 

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
        return render(request, 'registration/reg_form.html', {'form': form})


def login(request):
    print ('loglogint')
    print(request.GET)
    if request.method == 'GET':
        username = request.GET['username']
        password = request.GET['password']
        status = authenticate(username = username, password = password)
        print ('inside login')
        if status:
            return redirect("app/home")
        else:
            return HttpResponse('alert(notok)')

@login_required
def view_profile(request):
    print('*' * 10) 
    print(request)
    print(request.GET)
    print(request.user)
    print(type(request.user))
    args = {'username': 'abcd'}
    return JsonResponse(args)

@login_required
def edit_profile(request):
    if request.method =='POST':
        form = EditProfileForm(request.POST, instance = request.user)
        if form.is_valid:
            form.save()
            #return redirect('app/view_profile')
            return HttpResponsePermanentRedirect(reverse('app/view_profile'))
    else:
        form = EditProfileForm(instance = request.user)
        args = {'form': form }
        return render(request, 'registration/edit_profile.html', args)

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
        return render(request, 'registration/change_password.html', args)


class HomeView(TemplateView):
    template_name = 'registration/create_request.html'
    def get(self, request):
        user_is_present = reg_conference.objects.filter(user=request.user)
        args = {'user': request.user }
        if user_is_present:
            return render(request, 'registration/request_already_created.html', args)
        form = HomeForm() 
        return render(request, self.template_name, { 'form': form })

    def post(self, request):
        form = HomeForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return render(request, 'registration/request_confirmation.html')
        else:
            error = "Input's you given are not correct. Please give the correct input details" 
            args = {'form': form, 'error': error}
            return render(request, self.template_name, args)


def request_details(request):
    args = {'user': request.user }
    try:
        user_details = reg_conference.objects.get(user=request.user)
    except Exception as exc:
        return render(request, 'registration/user_not_registered.html', args)
    else:
        return render(request, 'registration/user_request_details.html', {'user_details': user_details})

