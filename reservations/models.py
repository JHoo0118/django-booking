import datetime
from django.utils import timezone
from django.db import models
from django.utils import timezone
from core import models as core_models


class BookedDay(core_models.TimeStampedModel):
    day = models.DateField(verbose_name="예약 날짜")
    reservation = models.ForeignKey(
        "Reservation", verbose_name="예약", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "예약일"
        verbose_name_plural = "예약일"

    def __str__(self):
        return str(self.day)


class Reservation(core_models.TimeStampedModel):

    """ Reservation Model Definition """

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "대기 중"),
        (STATUS_CONFIRMED, "수락됨"),
        (STATUS_CANCELED, "취소됨"),
    )

    status = models.CharField(
        max_length=12,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        verbose_name="예약 상태",
    )

    check_in = models.DateField(verbose_name="체크인")
    check_out = models.DateField(verbose_name="체크아웃")
    guest = models.ForeignKey(
        "users.User",
        related_name="reservations",
        on_delete=models.CASCADE,
        verbose_name="게스트",
    )
    room = models.ForeignKey(
        "rooms.Room",
        related_name="reservations",
        on_delete=models.CASCADE,
        verbose_name="숙소",
    )

    def __str__(self):
        return f"{self.room} - {self.check_in}"

    def in_progress(self):
        now = timezone.now().date()
        if self.status != "canceled":
            # return now >= self.check_in and now <= self.check_out
            return now <= self.check_out
        elif self.status == "canceled":
            return False

    in_progress.boolean = True
    in_progress.short_description = "진행중"

    def is_finished(self):
        now = timezone.now().date()
        is_finished = now > self.check_out
        if is_finished:
            BookedDay.objects.filter(reservation=self).delete()
        return is_finished

    is_finished.boolean = True
    is_finished.short_description = "만료됨"

    def get_now(self):
        return timezone.now().date()

    def save(self, *args, **kwargs):
        if self.pk is None:
            start = self.check_in
            end = self.check_out
            difference = end - start
            existing_booked_day = BookedDay.objects.filter(
                day__range=(start, end), reservation__room=self.room
            ).exists()

            if not existing_booked_day:
                super().save(*args, **kwargs)
                for i in range(difference.days + 1):
                    day = start + datetime.timedelta(days=i)
                    BookedDay.objects.create(day=day, reservation=self)
                return

        return super().save(*args, **kwargs)

    class Meta:

        verbose_name = "예약"
        verbose_name_plural = "예약"
        ordering = ["created"]
