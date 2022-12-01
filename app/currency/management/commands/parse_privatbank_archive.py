from django.core.management.base import BaseCommand
from currency.models import Rate


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument(
            '--date',
            help='Delete poll instead of closing it',
        )

    def handle(self, *args, **options):
        print(f'Rates count:', Rate.objects.count())
