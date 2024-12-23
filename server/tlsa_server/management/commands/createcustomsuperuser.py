from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import IntegrityError

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a superuser with a custom user_id'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=str, help='The user_id for the superuser')
        parser.add_argument('email', type=str, help='The email for the superuser')
        parser.add_argument('password', type=str, help='The password for the superuser')

    def handle(self, *args, **kwargs):
        user_id = kwargs['user_id']
        username = kwargs['user_id']
        email = kwargs['email']
        password = kwargs['password']

        try:
            User.objects.create_superuser(
                user_id=user_id,
                username=username,
                email=email,
                password=password,
                role='manager'
            )
            self.stdout.write(self.style.SUCCESS(f'Superuser created successfully with user_id: {user_id}'))
        except IntegrityError:
            self.stdout.write(self.style.ERROR(f'Superuser with user_id {user_id} already exists.'))
