from django.core.management import BaseCommand

from users.models import CustomUser


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = CustomUser.objects.create(
            email='notadmin@users.pro',
            is_staff=False,
            is_superuser=False
        )

        user.set_password('Canavakill1')
        user.save()
