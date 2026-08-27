from django.core.management.base import BaseCommand
from users.models import User


DEMO_ACCOUNTS = (
    ('demo_user', 'demo_user@example.invalid', 'Demo User', 'demo_user_password', User.Role.USER),
    ('demo_creator', 'demo_creator@example.invalid', 'Demo Creator', 'demo_creator_password', User.Role.CREATOR),
)


class Command(BaseCommand):
    help = 'Create or reset the public evaluation demo accounts.'

    def handle(self, *args, **options):
        for username, email, name, password, role in DEMO_ACCOUNTS:
            user, _ = User.objects.get_or_create(username=username, defaults={'email': email, 'name': name})
            user.email = email
            user.name = name
            user.role = role
            user.role_selected = True
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Ready: {username}'))
