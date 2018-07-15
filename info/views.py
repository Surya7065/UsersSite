from django.shortcuts import render, get_object_or_404, reverse
from django.http import request, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .forms import UserForm


def index(request):
    """
    Helper function to render Index.html for the path /user/
    :param request
    :return: list of Users with template
    """

    user_list = User.objects.all()

    return render(request, 'info/index.html', {'user_list': user_list})


def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # form is valid
            # add the user to database
            # redirect to the index page
            user = User.objects.create_user(username=request.POST['first_name'] + request.POST['last_name'],
                                            email=request.POST['email'], password=request.POST['password'],
                                            first_name= request.POST['first_name'], last_name= request.POST['last_name'])
            user.save()
            message = 'form valid'
            return HttpResponseRedirect(reverse('info:index'))
        else:
            message = 'Form is invalid'
    else:
        message = 'Create user'
        form = UserForm()

    return render(request, 'info/add_user.html', {'form': form, 'message': message})


def delete_user(request, user_id):
    """
    Helper function to delete User from database
    :param request
    :return: Display status of the deleted user with message
    """
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    return HttpResponseRedirect(reverse('info:index'))
