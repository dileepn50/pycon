from django.contrib import admin

# Register your models here.
from app.models import UserProfile
from app.models import reg_conference, state_list
admin.site.site_header = 'Pycon 2017 Administration'


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'my_info', 'website', 'city', 'mobile_number')

    def my_info(self, obj):
        return obj.description
    def mobile_number(self, obj):
        return obj.phone
    def get_queryset(self, request):
        queryset = super(UserProfileAdmin, self).get_queryset(request)
        queryset = queryset.order_by('user')
        return queryset


    my_info.short_description = 'info'


admin.site.register(UserProfile, UserProfileAdmin)
class reg_conference_admin(admin.ModelAdmin):
    list_display = ('user', 'email_id', 'phone_number','first_name', 'approve_status')
    def email_id(self, obj):
        return obj.email

admin.site.register(reg_conference, reg_conference_admin)
admin.site.register(state_list)
