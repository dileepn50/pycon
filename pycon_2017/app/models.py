from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from localflavor.in_.in_states import STATE_CHOICES
from localflavor.in_.models import INStateField
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    description = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    website = models.URLField(default='')
    phone = models.CharField(default='', max_length=10)
    def __str__(self):
        return str(self.user)


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)

class state_list(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return str(self.name)

     
class reg_conference(models.Model):
    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=10)
    #phone_number = PhoneNumberPrefixWidget()
    email = models.EmailField()
    company = models.CharField(max_length=26)
    address = models.CharField(max_length=28)
    #state = INStateField(choices=STATE_CHOICES) 
    state = models.CharField(max_length=20)
    pincode = models.CharField(max_length=10)

    status_choices = (
            ('a', 'approved'),
            ('c', 'cancelled'),
            ('w', 'weightinglist'),
            ('y', 'yet to check')
            )
    approve_status = models.CharField(max_length=1, choices=status_choices, default='y', blank=True, help_text='status check')
    def __str__(self):
        return str(self.user)

