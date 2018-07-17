"""user_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'info'

urlpatterns = [
    # /user/
    path('', views.index, name='index'),

    # /user/add/
    path('add/', views.add_user, name='add_user'),

    # /user/{{id}}/delete/
    path('<int:user_id>/delete', views.delete_user, name='delete_user'),

    # /user/{{id}}/edit/
    path('<int:user_id>/edit', views.edit_user, name='edit_user'),

    # /user/login/
    path('login', views.login_user, name='login'),

    # /user/logout/
    path('logout', views.logout_user, name='logout'),

    # /user/myaccount/
    path('myaccount/', views.my_account, name='my_account'),

    path('forgot_password/', views.forgot_pass, name='forgot_pass'),

]
