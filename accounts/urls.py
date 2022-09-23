import django.conf.urls
import django.contrib.auth.views
from django.urls import path

import accounts.views

urlpatterns = [

    path('login/', django.contrib.auth.views.LoginView.as_view(template_name='auth/login.html'), name="login"),
    path('logout/', accounts.views.logout, name="logout"),
    path('register/', accounts.views.register, name="register"), ]
