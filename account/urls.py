from django.conf.urls import url
from .views import dashboard, ProfileView,ELoginView, logout_view, register, EditProfileView
from django.contrib.auth.views import *


urlpatterns = [
    url(r'^$', dashboard, name='dashboard'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(r'^login/$', ELoginView.as_view(), name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^password-change/$', password_change, name='password_change'),
    url(r'^password-change/done/$', password_change_done, name='password_change_done'),
    url(r'^password-reset/$', password_reset, name='password_reset'),
    url(r'^password-reset/done/$', password_reset_done, name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', password_reset_confirm, name='password_reset_confirm'),
    url(r'^password-reset/complete/$', password_reset_complete, name='password_reset_complete'),
    url(r'^register/$', register, name='register'),
    url(r'^edit/$', EditProfileView.as_view(), name='edit'),


]

