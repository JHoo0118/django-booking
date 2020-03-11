from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User


class Command(BaseCommand):

    help = "유저 생성 명령어"

    def add_arguments(self, parser):
        parser.add_argument("--number", default=2, type=int, help="생성할 유저의 수")

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        seeder.add_entity(User, number, {"is_staff": False, "is_superuser": False})
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"유저 {number}명이 생성되었습니다."))
