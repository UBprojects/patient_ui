import random

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User as AU
from django.shortcuts import render, redirect
from django.urls import reverse

from patient_ui.models import *


def index(request):
    return redirect(reverse('dashboard'))


def login(request):
    if request.user.is_authenticated:
        redirect_url = request.GET.get("next", "/")
        return redirect(redirect_url)
    else:
        if request.method != "POST":
            context_data = {'metadata': {'title': 'Login'}}
            return render(request, 'patient_ui/auth/login.html', context=context_data)
        else:
            username = request.POST.get('username', None)
            if username:
                username = username.lower()
            password = request.POST.get('password', None)
            user = authenticate(username=username, password=password)
            redirect_url = request.get_full_path()
            if not user:
                messages.error(request, 'Oops, Incorrect username and/or password')
            elif user.is_active:
                auth_login(request, user)
            return redirect(redirect_url)


def forgot_password(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))
    else:
        if request.method != "POST":
            context_data = {'metadata': {'title': 'Forgot Password'}}
            return render(request, 'patient_ui/auth/forgot_password.html', context=context_data)
        else:
            email = request.POST.get('email', None)
            username = request.POST.get('username', None)
            user_obj = AuthUser.objects.filter(email=email, username=username, is_active=1)
            if user_obj.exists():
                n_digit = 6
                range_start = 10 ** (n_digit - 1)
                range_end = (10 ** n_digit) - 1
                new_password = str(random.randint(range_start, range_end))
                auth_obj = AU.objects.get(id=user_obj.first().id)
                auth_obj.set_password(new_password)
                auth_obj.save()

                # send email here
                if not settings.DEBUG:
                    first_name = user_obj.first().first_name
                    data_dict = {'first_name': first_name,
                                 'new_password': new_password}
                    email_subject, email_message = email_body.forgot_email(data_dict)
                    send_ses_email(email_subject, email_message, [email])

                user_info_obj = UserInfo.objects.filter(auth_user=user_obj).first()
                messages.success(request, 'We have sent you a new password on your email.')
                redirect_url = reverse('promoter_login') if user_info_obj.role == UserInfo.ROLE_PROMOTER else reverse(
                    'login')
            else:
                messages.error(request, 'Sorry, no such account found.')
                redirect_url = reverse('forgot_password')
                if 'next' in request.GET:
                    if request.GET['next'] != reverse('logout'):
                        redirect_url = request.GET['next']
            return redirect(redirect_url)


def logout(request):
    auth_logout(request)
    request.session.flush()
    return redirect(reverse('login'))


@login_required(login_url=settings.LOGIN_URL)
def my_profile(request):
    if request.method == 'POST':
        fname = request.POST.get("fname", None)
        lname = request.POST.get("lname", None)
        city_id = request.POST.get("city_id", None)
        phone = request.POST.get("phone", None)

        auth_user = AuthUser.objects.filter(id=request.user.id, is_active=True).first()
        if fname:
            auth_user.first_name = fname
        if lname:
            auth_user.last_name = lname
        auth_user.save()

        user_info = UserInfo.objects.filter(auth_user_id=request.user.id, auth_user__is_active=True).first()
        if phone:
            user_info.phone = phone
        if city_id:
            user_info.city_id = city_id
        user_info.save()

        messages.success(request, 'Your profile has been updated successfully')
        return redirect(reverse('my_profile'))
    else:
        user_info = UserInfo.objects.get(auth_user_id=request.user.id)
        cities = City.objects.filter(active=True).order_by("name")
        context_data = {'auth_info': user_info.auth_user,
                        'user_info': user_info,
                        'cities': cities,
                        'metadata': {'title': 'My profile'}}
        return render(request, 'patient_ui/auth/my_profile.html', context=context_data)


@login_required(login_url=settings.LOGIN_URL)
def change_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password', False)
        confirm_password = request.POST.get('confirm_password', False)

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
        else:
            user = AU.objects.filter(id=request.user.id, is_active=True).first()
            user.set_password(confirm_password)
            user.save()

            user = authenticate(username=request.user.username, password=confirm_password)
            auth_login(request, user)

            messages.success(request, "Your password has been changed.")
    return redirect(reverse('my_profile'))


def error503(request):
    data = {'error_code': 'Maintenance Mode ON',
            'error_message': "We are currently under maintenance. We will be back up soon."}
    return render(request, 'website/theme/error.html', data)


def error500(request):
    data = {'error_code': '500! Error',
            'error_message': "Unexpected error occurred. Our technology team is looking into it."}
    return render(request, 'website/theme/error.html', data)


def error404(request):
    data = {'error_code': '404! Error',
            'error_message': "Looks like you landed on the wrong planet."}
    return render(request, 'website/theme/error.html', data)


def error403(request):
    data = {'error_code': '403! Error',
            'error_message': "Please refresh the page and try again."}
    return render(request, 'website/theme/error.html', data)
