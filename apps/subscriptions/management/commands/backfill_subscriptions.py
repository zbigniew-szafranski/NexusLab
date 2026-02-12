from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from apps.subscriptions.models import UserSubscription


class Command(BaseCommand):
    help = 'Create UserSubscription for existing users who lack one.'

    def handle(self, *args, **options):
        users_without_sub = User.objects.filter(subscription__isnull=True)
        count = 0
        for user in users_without_sub:
            UserSubscription.objects.create(user=user)
            count += 1
        self.stdout.write(self.style.SUCCESS(f'Created {count} subscription(s).'))
