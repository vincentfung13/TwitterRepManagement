from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, **options):
        from twitter_services.tweet_processing.batch_processing.batch_processors import ReputationMonitor
        monitor = ReputationMonitor()
        monitor.scan()