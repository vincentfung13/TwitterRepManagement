from django.shortcuts import render
from django.contrib.postgres.aggregates import ArrayAgg
from django.views.generic import View
from .models import Tweet, Statistics
from tweet_processing import utility
from user_handle import utility as user_util
from datetime import datetime, timedelta
import pytz
import forms
import urllib


class TweetsFilter(View):
    def get(self, request, entity, dimension=None):
        form = forms.DateTweetForm(entity=entity, reputation_dimension=dimension)
        time_threshold = datetime.now(pytz.utc) - timedelta(days=5)
        if dimension is not None:
            tweets = Tweet.objects.filter(tweet__related_entity=entity,
                                          tweet__reputation_dimension=dimension,
                                          created_at__gt=time_threshold).order_by('-created_at')
        else:
            tweets = Tweet.objects.filter(tweet__related_entity=entity,
                                          created_at__gt=time_threshold).order_by('-created_at')

        context = {
            'form': form,
            'entity': entity,
            'entities_list': utility.entities_list,
            'dimension_list': utility.dimension_list,
            'Dimension': dimension,
        }
        context.update(utility.get_view_content(request, tweets))

        return render(request, 'twitter_services/tweets_filter.html', context)

    def post(self, request, entity, dimension=None):
        form = forms.DateTweetForm(request.POST, entity=entity, reputation_dimension=dimension)

        if form.is_valid():
            entity = form.cleaned_data['entity']
            reputation_dimension = form.cleaned_data['reputation_dimension']
            date = form.cleaned_data['date']

            if dimension is not None:
                tweets = Tweet.objects.filter(tweet__related_entity=entity,
                                              tweet__reputation_dimension=reputation_dimension,
                                              created_at__year=str(date.year),
                                              created_at__month=str(date.month),
                                              created_at__day=str(date.day)).order_by('-created_at')
            else:
                tweets = Tweet.objects.filter(tweet__related_entity=entity,
                                              created_at__year=str(date.year),
                                              created_at__month=str(date.month),
                                              created_at__day=str(date.day)).order_by('-created_at')

            context = {
                'form': form,
                'entity': entity,
                'entities_list': utility.entities_list,
                'dimension_list': utility.dimension_list,
                'Dimension': reputation_dimension,
            }
            context.update(utility.get_view_content(request, tweets))

            return render(request, 'twitter_services/tweets_filter.html', context)
        else:
            return user_util.json_response(-1, msg=form.errors)


class Graphs(View):
    def get(self, request, chart, entity, dimension=None):
        tweets_count_list = list()
        reputation_scores = list()
        negative_count_list = list()
        date_time_list = list()

        # Orderable ArrayAgg is not out yet
        f = lambda dimension_para: 'Whole' if dimension_para is None else dimension_para
        stat_querysets = list(Statistics.objects.filter(related_entity=entity,
                                                        reputation_dimension=f(dimension)).order_by('timestamp')[:5])
        for stat_queryset in stat_querysets:
            tweets_count_list.append(stat_queryset.total_tweets_count)
            reputation_scores.append(float("{0:.2f}".format(stat_queryset.reputation_score)))
            negative_count_list.append(stat_queryset.negative_count)
            date_time_list.append(str(stat_queryset.timestamp))

        context = {
            'chart': chart,
            'entity': entity,
            'dimension': dimension,
            'tweets_count_list': tweets_count_list,
            'reputation_scores': reputation_scores,
            'negative_count_list': negative_count_list,
            'date_time_list': date_time_list
        }

        return render(request, 'twitter_services/graphs.html', context)