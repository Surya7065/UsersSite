from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, reverse
from django.http import request, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .forms import UserForm
from django.conf import settings
from .models import VerificationToken
from django.utils.crypto import get_random_string


def index(request):
    """
    Helper function to render Index.html for the path /user/
    :param request
    :return: list of Users with template
    """

    if request.user.is_authenticated:
        user_list = User.objects.all()
        return render(request, 'info/mdg/index.html', {'user_list': user_list})
    else:
        return HttpResponseRedirect(reverse('info:login'))


def add_user(request):
    error_message = None
    if request.method == 'POST':
        pass
        form = UserForm(request.POST)
        if form.is_valid():
            # form is valid
            # add the user to database
            # redirect to the index page
            try:
                user = User.objects.create_user(username=request.POST['first_name'] + request.POST['last_name'],
                                                email=request.POST['email'], password=request.POST['password'],
                                                first_name=request.POST['first_name'],
                                                last_name=request.POST['last_name'])

                return HttpResponseRedirect(reverse('info:index'))
            except IntegrityError as e:
                error_message = "User name already taken"
        else:
            error_message = 'Form is invalid'
    else:
        message = 'Create user'
        form = UserForm()

    return render(request, 'info/mdg/add_user.html',
                  {'form': form, 'message': 'Create User', 'error_message': error_message})


def delete_user(request, user_id):
    """
    Helper function to delete User from database
    :param user_id: User id primary key
    :param request
    :return: Display status of the deleted user with message
    """
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    return HttpResponseRedirect(reverse('info:index'))


def edit_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # form is valid
            # add the user to database
            # redirect to the index page
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.password = request.POST['password']
            user.save()
            message = 'form valid'
            return HttpResponseRedirect(reverse('info:index'))
        else:
            message = 'Form is invalid'
    else:
        message = 'Edit user'
        data = {'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email,
                'password': user.password}
        form = UserForm(initial=data)

    return render(request, 'info/mdg/add_user.html', {'form': form, 'message': message})


def login_user(request):
    error_message = None
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            x = User.objects.get(email=email)
            user = authenticate(username=x.username, password=password)
            if user is None:
                # User does not exist
                error_message = "Wrong credentials"
            else:
                login(request, user)
                return HttpResponseRedirect(reverse('info:index'))
        except User.DoesNotExist:
            error_message = "Wrong credentials"

    return render(request, 'info/mdg/login_page.html', {'error_message': error_message})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('info:login'))


def my_account(request):
    if request.user.is_authenticated:
        return render(request, 'info/mdg/account.html', {})
    else:
        return HttpResponseRedirect(reverse('info:login'))


def forgot_pass(request):
    error = None
    if request.method == 'POST':
        # validate email
        email = request.POST['email']
        user = User.objects.get(email=email)
        if user is None:
            # User does not exists
            error = 'Email id not registered'
        else:
            # send verification link
            try:
                vt = VerificationToken.objects.get(user=user)
                unique_id = vt.token
            except VerificationToken.DoesNotExist:
                unique_id = get_random_string(64)
                vt = VerificationToken.objects.create(token=unique_id, user=user, is_token_valid=True)

            subject = 'Password Reset Requested'
            message = 'Click the below link to reset your password\n' + '127.0.0.1:8000/user/reset_password/' + unique_id
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, email_from, recipient_list)
            return HttpResponse('Email Sent')
    return render(request, 'info/mdg/forgot_password.html', {'error': error})


def reset_pass(request, token):
    message = None

    if request.method == 'POST':
        password = request.POST['password']
        pw_a = request.POST['pw_a']
        if password != pw_a:
            # passwords do not match display error
            return render(request, 'info/mdg/reset_password.html', {'error_message': 'Passwords do not match'})
            pass
        else:
            vf = VerificationToken.objects.get(token=token)
            user = vf.user
            user.set_password(password)
            user.save()
            vf.delete()
            return HttpResponseRedirect(reverse('info:login'))

    else:
        try:
            vf = VerificationToken.objects.get(token=token)
            if vf.is_token_valid:
                message = 'token valid'
                # display password reset form
                return render(request, 'info/mdg/reset_password.html')
            else:
                # token not valid
                message = 'token is expired'
                pass
        except VerificationToken.DoesNotExist:
            # Verification token does not exist
            message = 'Unauthorised entry'

    return HttpResponse(message)
