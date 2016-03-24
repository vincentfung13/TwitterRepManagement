from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        from twitter_services.tweet_processing.batch_processing.batch_processors import ReputationMonitor
        monitor = ReputationMonitor()
        monitor.scan()