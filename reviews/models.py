from django.db import models
from core import models as core_models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse


class Review(core_models.TimeStampedModel):

    """ Review Model Definition """

    review = models.TextField(verbose_name="후기")
    accuracy = models.IntegerField(
        verbose_name="정확성", validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    communication = models.IntegerField(
        verbose_name="의사소통", validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    cleanliness = models.IntegerField(
        verbose_name="청결도", validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    location = models.IntegerField(
        verbose_name="위치", validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    check_in = models.IntegerField(
        verbose_name="체크인", validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    value = models.IntegerField(
        verbose_name="가치", validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    user = models.ForeignKey(
        "users.User",
        related_name="reviews",
        on_delete=models.CASCADE,
        verbose_name="사용자",
    )
    room = models.ForeignKey(
        "rooms.Room",
        related_name="reviews",
        on_delete=models.CASCADE,
        verbose_name="숙소",
    )

    def __str__(self):
        return f"{self.review} - {self.room}"

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})

    def rating_average(self):
        avg = (
            self.accuracy
            + self.communication
            + self.cleanliness
            + self.location
            + self.check_in
            + self.value
        ) / 6
        return round(avg, 2)

    rating_average.short_description = "평점"

    class Meta:

        verbose_name = "후기"
        verbose_name_plural = "후기"
        ordering = ("-created",)
