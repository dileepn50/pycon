from django.conf.urls import url
from django.contrib.auth import views as auth_views

from app.views import login, base, HomeView
from . import views
urlpatterns = [
        url('^$', base),
        url('home$', base),
        url('app/$', base),
        url(r'login_page$', auth_views.login, {'template_name': 'registration/login.html'}),
        url(r'logout_page$', auth_views.logout, {'template_name': 'registration/logout.html'}),
        url(r'login$', login),
        url(r'register$', views.register),
        url(r'view_profile$', views.view_profile, name = 'index'),
        url(r'edit_profile$', views.edit_profile, name = 'edit_super'),
        url(r'change_password$', views.change_password),
        url(r'reset_password$', auth_views.password_reset),
        url(r'reset_password_done$', auth_views.password_reset_done, name = 'password_reset_done'),
        url(r'reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, name = 'password_reset_confirm'),
        url(r'reset_password_complete', auth_views.password_reset_complete, name = 'password_reset_complete'),

        url('post_request', HomeView.as_view()),
        url('request_details$', views.request_details),
        ]
