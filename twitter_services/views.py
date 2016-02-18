from django.shortcuts import render
from django.views.generic import View
from .models import Tweet
from user_handle.models import UserEntity
from django.contrib.auth.models import User
from tweet_processing import utility
from geocoding.geocoders import LocalGeocoder


class TweetsFilter(View):
    def get(self, request, entity, dimension=None):
        if dimension is not None:
            tweets = Tweet.objects.filter(tweet__related_entity=entity,
                                          tweet__reputation_dimension=dimension).order_by('-created_at')
        else:
            tweets = Tweet.objects.filter(tweet__related_entity=entity).order_by('-created_at')

        tweets_filtered = [tweet_orm.tweet for tweet_orm in tweets]

        geocoder = LocalGeocoder()
        coordinates = geocoder.geocode_many(tweets_filtered)
        latitudes = [coordinate[0] for coordinate in coordinates]
        longitudes = [coordinate[1] for coordinate in coordinates]

        # Get users' list of interest
        user = User.objects.get(username=request.user.username)
        interest_list = [ue_orm.entity for ue_orm in UserEntity.objects.filter(user=user)]

        context = {
            'tweets': tweets_filtered[:100],
            'entity': entity,
            'entities_list': utility.entities_list,
            'dimension_list': utility.dimension_list,
            'latitudes': latitudes,
            'longitudes': longitudes,
            'Dimension': dimension,
            'interest_list': interest_list
        }

        return render(request, 'twitter_services/tweets_filter.html', context)


# TODO: Collect more data and generate stats dynamically
class Graphs(View):
    def get(self, request, entity, dimension=None):
        tweets_count_list = [294, 533, 400, 600, 700]
        reputation_scores =[-5.4, 3.44, 0.99, -1.3, 2.2]
        negative_percentages = [0.5, 0.08, 0.2, 0.21, 0.12]
        date_time_list = ['2016-02-01', '2016-02-02', '2016-02-03', '2016-02-04', '2016-02-05']

        context = {
            'entity': entity,
            'dimension': dimension,
            'tweets_count_list': tweets_count_list,
            'reputation_scores': reputation_scores,
            'negative_percentage': negative_percentages,
            'date_time_list': date_time_list
        }

        return render(request, 'twitter_services/graphs.html', context)