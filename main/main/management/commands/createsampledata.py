from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from main.models_factory import GoodFactory, SellerFactory


class Command(BaseCommand):
    """
    Management command for creating sample data
    """

    def add_arguments(self, parser):
        parser.add_argument('model', nargs=1, type=str)
        parser.add_argument('good_name', nargs=1, type=str)

    def handle(self, *args, **options):
        acceptable_models = ['good', 'seller']
        model = options['model'][0]
        object_name = options['good_name'][0]
        if model not in acceptable_models:
            raise CommandError(f'Model {model} is not exist or'
                               f' not acceptable for generation sample data')
        else:
            if model == 'good':
                try:
                    _ = GoodFactory(name=object_name)
                except IntegrityError as e:
                    if 'unique constraint' in str(e).lower():
                        raise CommandError(f'Good with name \'{object_name}\' already exist')
            if model == 'seller':
                try:
                    _ = SellerFactory(name=object_name)
                except IntegrityError as e:
                    if 'unique constraint' in str(e).lower():
                        raise CommandError(f'Seller with name \'{object_name}\' already exist')

                self.stdout.write(self.style.SUCCESS(f'Successfully generated data for \'{model}\' model'))