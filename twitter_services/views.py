from django.shortcuts import render
from django.views.generic import View
from .models import Tweet
from tweet_processing import utility
from user_handle import utility as user_util
from datetime import datetime, timedelta
import pytz
import forms


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


# TODO: Collect more data and generate stats dynamically
class Graphs(View):
    def get(self, request, chart, entity, dimension=None):
        tweets_count_list = [294, 533, 400, 600, 700]
        reputation_scores =[-5.4, 3.44, 0.99, -1.3, 2.2]
        negative_count_list = [200, 300, 133, 289, 468]
        date_time_list = ['2016-02-01', '2016-02-02', '2016-02-03', '2016-02-04', '2016-02-05']

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