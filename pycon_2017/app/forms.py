from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm 
from app.models import reg_conference
import localflavor.in_.forms as loc_in 
from phonenumber_field.widgets import PhoneNumberPrefixWidget

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)


    class Meta:
        model = User
        fields = ('username',
                'first_name',
                'last_name',
                'email',
                'password1',
                'password2'
                )
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name',
                'last_name',
                'email',
                'password',
                )


class HomeForm(forms.ModelForm):
    #phone_number = PhoneNumberPrefixWidget() 
    #phone_number = loc_in.STATE_CHOICES
    #state = loc_in.INStateField()
    pincode = loc_in.INZipCodeField()
    class Meta:
        model = reg_conference 
        fields = ('first_name', 'last_name', 'phone_number', 'email', 'company', 'address', 'state', 'pincode', 'uploaded_file')




