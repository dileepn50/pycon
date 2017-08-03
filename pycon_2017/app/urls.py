from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt

#from app.views import base, HomeView, edit_profile, view_profile, get_states, admin_user, reg_user_details, add_state, request_status

from app import views as app_views
urlpatterns = [
        url('^$', app_views.base),
        url('home$', app_views.base),
        url(r'admin$',app_views.admin_user),
        url('app/$', app_views.base),
        url(r'login_page$', csrf_exempt(auth_views.login), {'template_name': 'login.html'}),
        url(r'logout_page$', csrf_exempt(auth_views.logout), {'template_name': 'logout.html'}),
        url(r'register$', app_views.register),
        url(r'request_status', app_views.request_status),
        url(r'view_profile$', app_views.ViewProfile.as_view(), name = 'index'),
        url(r'edit_profile$', csrf_exempt(app_views.EditProfile.as_view()), name = 'edit_super'),
        url(r'change_password$', app_views.change_password),
        url(r'reset_password$', auth_views.password_reset),
        url(r'reset_password_done$', auth_views.password_reset_done, name = 'password_reset_done'),
        url(r'reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, name = 'password_reset_confirm'),
        url(r'reset_password_complete', auth_views.password_reset_complete, name = 'password_reset_complete'),
        url('post_request$', csrf_exempt(app_views.HomeView.as_view())),
        url('request_details$', app_views.request_details),
        url('state_list$', app_views.get_states),
        url('get_user_details/$',csrf_exempt(app_views.RegUserDetails.as_view())),
        url('get_user_details/([a-zA-Z]*)$',csrf_exempt(app_views.RegUserDetails.as_view())),
        url('add_state$', csrf_exempt(app_views.add_state)),
        ]


