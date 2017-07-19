from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt

from app.views import base, HomeView, edit_profile, view_profile, get_states, admin_user

from . import views
urlpatterns = [
        url('^$', base),
        url('home$', base),
        url(r'admin$', admin_user),
        url('app/$', base),
        url(r'login_page$', csrf_exempt(auth_views.login), {'template_name': 'login.html'}),
        url(r'logout_page$', csrf_exempt(auth_views.logout), {'template_name': 'logout.html'}),
        url(r'register$', views.register),
        url(r'view_profile$', view_profile.as_view(), name = 'index'),
        url(r'edit_profile$', csrf_exempt(edit_profile.as_view()), name = 'edit_super'),
        url(r'change_password$', views.change_password),
        url(r'reset_password$', auth_views.password_reset),
        url(r'reset_password_done$', auth_views.password_reset_done, name = 'password_reset_done'),
        url(r'reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, name = 'password_reset_confirm'),
        url(r'reset_password_complete', auth_views.password_reset_complete, name = 'password_reset_complete'),

        url('post_request$', csrf_exempt(HomeView.as_view())),
        url('request_details$', views.request_details),
        url('state_list$', views.get_states),
        ]
