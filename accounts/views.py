from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.forms import UserLoginForm, UserRegistrationForm


# Create your views here.
def index(request):
    '''return the index.html file'''
    return render(request, 'index.html')


@login_required  # this ensures users that are NOT logged in can't get access to the logout page which could cause bugs
def logout(request):
    '''Log the user out'''
    auth.logout(request)
    messages.success(request, "You have successfully been logged out!")
    return redirect(reverse('index'))  # reverse allows us to pass the name of a url instead of the view name


def login(request):
    '''return a login page'''
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password'])

            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully logged in!")
                return redirect(reverse('index'))
            else:
                login_form.add_error(None, "Your username or password is invalid")
    else:
        login_form = UserLoginForm()
    return render(request, 'login.html', {"login_form": login_form})


def registration(request):
    '''render the registration page'''
    if request.user.is_authenticated:
        return redirect(reverse('index'))

    if request.method == 'POST':
        registration_form = UserRegistrationForm(request.POST)

        if registration_form.is_valid():
            registration_form.save()

            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password1'])

            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully registered!")
                return redirect(reverse('index'))
            else:
                messages.error(request, "Unable to register your account at this time")

    else:
        registration_form = UserRegistrationForm()
    return render(request, 'registration.html', {
        "registration_form": registration_form})


def user_profile(request):
    '''The users profile page'''
    user = User.objects.get(email=request.user.email)
    return render(request, 'profile.html', {"profile": user})
