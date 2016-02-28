import forms
import json
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, get_user
from django.core.urlresolvers import reverse
from django.db import transaction
from user_handle.models import UserEntity, UserMessage, Message
from user_handle import utility as user_util
from twitter_services.geocoding.geocoders import LocalGeocoder
from twitter_services.tweet_processing import utility as tweet_util


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
        form = forms.EntityForm()
        # Display user's list of interest
        interest_list = [ue_orm.entity for ue_orm in UserEntity.objects.filter(user=get_user(request))]
        remaining_entities = [entity for entity in tweet_util.entities_list if entity not in interest_list]
        return render(request, 'user_handle/entity.html', {'form': form,
                                                           'interest_list': interest_list,
                                                           'remaining_entities': remaining_entities, })

    # Adds the entity in to the database and sends a message to the front end
    def post(self, request):
        if request.POST['action'] == 'add':
            user_util.add_interested(request.user, request.POST['entity'])
        elif request.POST['action'] == 'remove':
            user_util.remove_entity(request.user, request.POST['entity'])
        else:
            return user_util.json_response(-1, msg=u'invalid action')
        # Redirect to user index page on success
        return HttpResponseRedirect(reverse('user_handle:Index'))


# Index page for each user (showing the clickable entity list they are interested in)
class Index(View):
    def get(self, request):
        entity_list = [pair.entity for pair in UserEntity.objects.filter(user=get_user(request))]
        interest_list = [ue_orm.entity for ue_orm in UserEntity.objects.filter(user=get_user(request))]

        context = {'username': request.user.username,
                   'entity_list': entity_list,
                   'interest_list': interest_list,
                   'interest_list_jsonify': json.dumps(interest_list),
                   'dimension_list': tweet_util.dimension_list,
                   }
        return render(request, 'user_handle/index.html', context)


class MessageView(View):
    @transaction.atomic
    def get(self, request, message_id):
        message = Message.objects.get(pk=message_id)
        tweets = [tweet_orm.tweet for tweet_orm in message.tweet.all().order_by('-created_at')]
        message.read = True
        message.save()
        interest_list = [ue_orm.entity for ue_orm in UserEntity.objects.filter(user=get_user(request))]

        topic_list = message.topic_str.split('\n')
        keywords = []
        weights = []

        for topic_tuple in topic_list:
            keyword = topic_tuple.split(',')[0]
            weight = float(topic_tuple.split(',')[1])

            keywords.append(str(keyword))
            weights.append(weight)

        geocoder = LocalGeocoder()
        coordinates = geocoder.geocode_many(tweets)
        latitudes = [coordinate[0] for coordinate in coordinates]
        longitudes = [coordinate[1] for coordinate in coordinates]

        return render(request, 'user_handle/message.html', {'tweets': tweets[:100],
                                                            'message': message,
                                                            'interest_list': interest_list,
                                                            'topic_keywords': keywords,
                                                            'keywords_weight': weights,
                                                            'latitudes': latitudes,
                                                            'longitudes': longitudes
                                                            })


# The view to manage server-to-user messages
class MessageInbox(View):
    def get(self, request):
        messages_unread = []
        messages_read = []
        for um_pair in UserMessage.objects.filter(user=get_user(request)).order_by('-message'):
            messages_unread.extend(um_pair.message.filter(read=False))
            messages_read.extend(um_pair.message.filter(read=True))

        interest_list = [ue_orm.entity for ue_orm in UserEntity.objects.filter(user=get_user(request))]
        return render(request, 'user_handle/inbox.html', {'messages_read': messages_read,
                                                          'messages_unread': messages_unread,
                                                          'interest_list': interest_list})


