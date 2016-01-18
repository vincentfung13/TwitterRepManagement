from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
import forms
import utility


# Create your views here.
class Register(View):
    # If it is a get, display the form for people to enter detail
    def get(self, request):
        form = forms.RegisterForm()
        return render(request, 'user_handle/register.html', {'form': form})

    # Login otherwise
    def post(self, request):
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            if utility.check_exist(username, email):
                return HttpResponse('username or email already exists')
            else:
                utility.save_user(username, password, email)
                # TODO: redirect to index page
                return HttpResponse('successfully registered')
        else:
            return utility.json_response(-1, msg=form.errors)


class Login(View):
    # If it is a get, display the form for people to enter detail
    def get(self, request):
        form = forms.LoginForm()
        return render(request, 'user_handle/login.html', {'form': form})

    # Login otherwise
    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Login successfully')
                else:
                    return utility.json_response(-1, msg=u'The account is not activated, please contact administrator')
            else:
                return utility.json_response(-1, msg=u'Username or password is incorrect')
        else:
            return utility.json_response(-1, msg=form.errors)


class Logout(View):
    def get(self, request):
        logout(request)
        # TODO: redirect to site main page
        return HttpResponse('Logout successfully')


class AddInterested(View):
    def get(self, request):
        form = forms.AddEntityForm()
        return render(request, 'user_handle/add_entity.html', {'form': form})

    # Adds the entity in to the database and sends a message to the front end
    def post(self, request):
        form = forms.AddEntityForm(request.POST)
        if form.is_valid():
            # Create a row in the database
            utility.add_interested(request.user, form.cleaned_data['entity'])
        else:
            return utility.json_response(-1, msg=form.errors)


# Index page for each user (showing the clickable entity list they are interested in)
class Index(View):
    def get(self, request, username):
        context = {}
        return render(request, 'user_handle/index.html', context)
