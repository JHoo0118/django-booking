from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):

    help = "슈퍼 유저 생성"

    def handle(self, *args, **options):
        admin = User.objects.get_or_none(username="admin")
        if not admin:
            User.objects.create_superuser("admin", "kik3078@naver.com", "1234")
            self.stdout.write("슈퍼유저가 생성되었습니다.")
        else:
            self.stdout.write("슈퍼유저가 존재합니다.")
