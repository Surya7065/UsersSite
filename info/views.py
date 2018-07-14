from django.shortcuts import render, get_object_or_404
from django.http import request, HttpResponse
from django.contrib.auth.models import User
from .forms import UserForm

def index(request):
    """
    Helper method to render Index.html for the path /user/
    :param request
    :return: list of Users
    """

    user_list = User.objects.all()

    return render(request, 'info/index.html', {'user_list': user_list})


def add_user(request):
    form = UserForm()
    return render(request, 'info/add_user.html', {'form': form})
