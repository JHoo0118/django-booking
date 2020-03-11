from django.db import models
from core import models as core_models


class List(core_models.TimeStampedModel):

    """ List Model Definition """

    name = models.CharField(max_length=80, verbose_name="이름")
    user = models.OneToOneField(
        "users.User", related_name="list", on_delete=models.CASCADE, verbose_name="사용자"
    )
    rooms = models.ManyToManyField(
        "rooms.Room", related_name="lists", blank=True, verbose_name="숙소"
    )

    def __str__(self):
        return self.name

    def count_rooms(self):
        return self.rooms.count()

    count_rooms.short_description = "숙소 개수"

    class Meta:

        verbose_name = "목록"
        verbose_name_plural = "목록"
        ordering = ["created"]
