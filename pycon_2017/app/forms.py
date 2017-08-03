from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import forms as auth_forms 

import localflavor.in_.forms as loc_in 

from app import models as app_models 

class RegistrationForm(auth_forms.UserCreationForm):
    email = forms.EmailField(required=True, help_text='enter valid email address')
    username = forms.CharField(required=True, help_text='enter username')

    class Meta:
        model = User
        fields = ('username',
                'email',
                'password1',
                'password2'
                )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class EditProfileForm(auth_forms.UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name',
                'last_name',
                'email',
                'password',
                )


class HomeForm(forms.ModelForm):
    pincode = loc_in.INZipCodeField()
    class Meta:
        model = app_models.reg_conference 
        fields = ('first_name', 'last_name', 'phone_number', 'email', 'company', 'address', 'state', 'pincode')



