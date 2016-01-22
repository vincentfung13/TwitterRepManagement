from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, get_user
from django.db import transaction
from user_handle.models import UserEntity, UserMessage, Message
import forms
from user_handle import utility
import json


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
                # Direct to index page on success
                return HttpResponse('/user_handle/%s/' % username)
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
                    return redirect('/user_handle/%s/' % username)
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


# Login required
class ManageInterested(View):
    def get(self, request, username):
        form_add = forms.EntityForm()
        form_delete = forms.EntityForm()
        # TODO: Display user's list of interest
        return render(request, 'user_handle/entity.html', {'form_add': form_add, 'form_delete': form_delete})

    # Adds the entity in to the database and sends a message to the front end
    def post(self, request, username, action):
        form = forms.EntityForm(request.POST)
        if form.is_valid():
            # Create a row in the database
            if action == 'add':
                utility.add_interested(request.user, form.cleaned_data['entity'])
            elif action == 'remove':
                utility.remove_entity(request.user, form.cleaned_data['entity'])
            else:
                return utility.json_response(-1, msg=u'invalid action')
            return HttpResponse('Action successful')
        else:
            return utility.json_response(-1, msg=form.errors)


# Login required
# Index page for each user (showing the clickable entity list they are interested in)
class Index(View):
    def get(self, request, username):
        entity_list = [pair.entity for pair in UserEntity.objects.filter(user=request.user)]
        context = {'username': username, 'entity_list': entity_list}
        return render(request, 'user_handle/index.html', context)


class MessageView(View):
    @transaction.atomic
    def get(self, request, username, message_id):
        message = Message.objects.get(pk=message_id)
        tweets = [json.dumps(utility.build_dict(tweet)) for tweet in message.tweet.all().order_by('-created_at')]
        message.read = True
        message.save()
        return render(request, 'user_handle/message.html', {'tweets': tweets, 'message': message})


# The view to manage server-to-user messages
class MessageInbox(View):
    def get(self, request, username):
        messages = []
        for um_pair in UserMessage.objects.filter(user=get_user(request)):
            messages.extend(um_pair.message.filter(read=False))
        return render(request, 'user_handle/inbox.html', {'messages': messages})


