from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, get_user
from django.core.urlresolvers import reverse
from django.db import transaction
from user_handle.models import UserEntity, UserMessage, Message
import forms
from user_handle import utility as user_util


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

            if user_util.check_exist(username, email):
                return HttpResponse('username or email already exists')
            else:
                user_util.save_user(username, password, email)
                # Direct to index page on success
                user = authenticate(username=username, password=password)
                login(request, user)
                return HttpResponseRedirect(reverse('user_handle:Index'))
        else:
            return user_util.json_response(-1, msg=form.errors)


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
                    return HttpResponseRedirect(reverse('user_handle:Index'))
                else:
                    return user_util.json_response(-1, msg=u'The account is not activated, please contact administrator')
            else:
                return user_util.json_response(-1, msg=u'Username or password is incorrect')
        else:
            return user_util.json_response(-1, msg=form.errors)


class Logout(View):
    def get(self, request):
        logout(request)
        # redirect to site main page
        return HttpResponseRedirect(reverse('MainPage'))


class ManageInterested(View):
    def get(self, request):
        form_add = forms.EntityForm()
        form_delete = forms.EntityForm()
        # Display user's list of interest
        return render(request, 'user_handle/entity.html', {'form_add': form_add, 'form_delete': form_delete})

    # Adds the entity in to the database and sends a message to the front end
    def post(self, request, action):
        form = forms.EntityForm(request.POST)
        if form.is_valid():
            # Create a row in the database
            if action == 'add':
                user_util.add_interested(request.user, form.cleaned_data['entity'])
            elif action == 'remove':
                user_util.remove_entity(request.user, form.cleaned_data['entity'])
            else:
                return user_util.json_response(-1, msg=u'invalid action')
            # Redirect to user index page on success
            return HttpResponseRedirect(reverse('user_handle:Index'))
        else:
            return user_util.json_response(-1, msg=form.errors)


# Index page for each user (showing the clickable entity list they are interested in)
class Index(View):
    def get(self, request):
        entity_list = [pair.entity for pair in UserEntity.objects.filter(user=request.user)]
        context = {'username': request.user.username, 'entity_list': entity_list}
        return render(request, 'user_handle/index.html', context)


class MessageView(View):
    @transaction.atomic
    def get(self, request, message_id):
        message = Message.objects.get(pk=message_id)
        tweets = [tweet_orm.tweet for tweet_orm in message.tweet.all().order_by('-created_at')]
        message.read = True
        message.save()
        return render(request, 'user_handle/message.html', {'tweets': tweets, 'message': message})


# The view to manage server-to-user messages
class MessageInbox(View):
    def get(self, request):
        messages = []
        for um_pair in UserMessage.objects.filter(user=get_user(request)):
            messages.extend(um_pair.message.filter(read=False))
        return render(request, 'user_handle/inbox.html', {'messages': messages})


