import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create the Render superuser if it does not exist"

    def handle(self, *args, **options):
        User = get_user_model()

        email = os.getenv("ADMIN_EMAIL")
        password = os.getenv("ADMIN_PASSWORD")

        if not email or not password:
            self.stdout.write(
                self.style.ERROR(
                    "ADMIN_EMAIL and ADMIN_PASSWORD environment variables are required."
                )
            )
            return

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
                "role": User.Role.MANAGEMENT,
            },
        )

        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f"Superuser created: {email}")
            )
        else:
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.role = User.Role.MANAGEMENT
            user.save()

            self.stdout.write(
                self.style.SUCCESS(f"Superuser updated: {email}")
            )