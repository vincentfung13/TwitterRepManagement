from TwitterRepManagement import settings
import csv
import string


class LocalGeocoder(object):
    def __init__(self):
        # Import world cities database
        with open(settings.BASE_DIR + '/resources/twitter_services/geocoder/cities15000.txt', 'r') as geonames_db:
            self.location_dict = {}
            for line in geonames_db:
                line = line.strip().split('\t')
                alternate = line[3].split(',')
                if len(alternate) == 1:
                    alternate = [line[1]]

                alternate = [filter(lambda x: x in string.printable, name).lower() for name in alternate
                             if len(filter(lambda x: x in string.printable, name)) > 1]

                lat = float(line[4])
                lon = float(line[5])

                self.location_dict.update(dict.fromkeys(alternate, [lat, lon]))

        # Import US states database
        with open(settings.BASE_DIR + '/resources/twitter_services/geocoder/us_states.csv') as us_states:
            us_states_file = csv.reader(us_states)
            for row in us_states_file:
                self.location_dict[row[0].lower()] = [float(row[2]), float(row[3])]

        # Import countries database
        with open(settings.BASE_DIR + '/resources/twitter_services/geocoder/countries.csv') as countries_latlon:
            countries = csv.reader(countries_latlon)
            for row in countries:
                self.location_dict[row[2].lower()] = [float(row[3]), float(row[4])]


    # Take a list of tweets and returns a list of coordinates accordingly
    # Location that doesn't have a match will be discarded
    def geocode_many(self, tweets):
        coordinates = []
        for tweet in tweets:
            location = tweet['user']['location']
            if location is not None:
                location = tweet['user']['location'].strip().split(',')[0]
                try:
                    coordinates.append(self.location_dict[location.lower()])
                except KeyError:
                    continue

        return coordinates

if __name__ == '__main__':
    import DjangoSetup
    from twitter_services.models import Tweet

    geocoder = LocalGeocoder()

    tweets = []
    for tweet_orm in Tweet.objects.all():
        tweets.append(tweet_orm.tweet)

    print len(geocoder.geocode_many(tweets))
