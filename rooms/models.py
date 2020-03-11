from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django_countries.fields import CountryField
from core import models as core_models
from cal import Calendar
from django.db.models import Max


class AbstractItem(core_models.TimeStampedModel):

    """ Abstract Item """

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):

    """ RoomType Model Definition """

    class Meta:
        verbose_name = _("숙소 유형")
        verbose_name_plural = _("숙소 유형")
        ordering = ["name"]


class Amenity(AbstractItem):

    """ Amenity Model Definition """

    class Meta:
        verbose_name = _("편의시설")
        verbose_name_plural = _("편의시설")
        ordering = ["name"]


class Facility(AbstractItem):

    """ Facility Model Definition """

    class Meta:
        verbose_name = _("시설")
        verbose_name_plural = _("시설")
        ordering = ["name"]


class HouseRule(AbstractItem):

    """ HouseRule Model Definition """

    class Meta:
        verbose_name = _("숙소 이용규칙")
        verbose_name_plural = _("숙소 이용규칙")
        ordering = ["name"]


class Photo(core_models.TimeStampedModel):

    """ Photo Model Definition """

    caption = models.CharField(_("설명"), max_length=80)
    file = models.ImageField(_("이미지"), upload_to="room_photos")
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption

    class Meta:
        verbose_name = _("사진")
        verbose_name_plural = _("사진")


class Room(core_models.TimeStampedModel):

    """ Room Model Definition """

    name = models.CharField(_("숙소명"), max_length=140)
    description = models.TextField(_("설명"))
    country = CountryField(_("국가"))
    city = models.CharField(_("도시"), max_length=80)
    price = models.IntegerField(_("가격"))
    address = models.CharField(_("주소"), max_length=140)
    guests = models.IntegerField(
        _("게스트"),
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        help_text="몇 명이 머무를 예정입니까?",
    )
    beds = models.IntegerField(
        _("침대"), validators=[MinValueValidator(1), MaxValueValidator(9)]
    )
    bedrooms = models.IntegerField(
        _("침실"), validators=[MinValueValidator(1), MaxValueValidator(9)]
    )
    baths = models.IntegerField(
        _("욕실"), validators=[MinValueValidator(1), MaxValueValidator(9)]
    )
    check_in = models.TimeField(_("체크인"))
    check_out = models.TimeField(_("체크아웃"))
    instant_book = models.BooleanField(_("즉시예약"), default=False)
    host = models.ForeignKey(
        "users.User", related_name="rooms", verbose_name="호스트", on_delete=models.CASCADE
    )
    room_type = models.ForeignKey(
        "RoomType",
        related_name="rooms",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="숙소 유형",
    )
    amenities = models.ManyToManyField(
        "Amenity", related_name="rooms", verbose_name="편의시설", blank=True
    )
    facilities = models.ManyToManyField(
        "Facility", related_name="rooms", verbose_name="시설", blank=True
    )
    house_rules = models.ManyToManyField(
        "HouseRule", related_name="rooms", verbose_name="숙소 이용규칙", blank=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating_average()
            return round(all_ratings / len(all_reviews), 2)
        return 0

    total_rating.short_description = "총 평점"

    def get_first_photo(self):
        try:
            (photo,) = self.photos.all()[:1]
            return photo.file.url
        except ValueError:
            return None

    def get_second_photo(self):
        try:
            (photo,) = self.photos.all()[1:2]
            return photo.file.url
        except ValueError:
            return None

    def get_third_photo(self):
        try:
            (photo,) = self.photos.all()[2:3]
            return photo.file.url
        except ValueError:
            return None

    def get_fourth_photo(self):
        try:
            (photo,) = self.photos.all()[3:4]
            return photo.file.url
        except ValueError:
            return None

    def get_fifth_photo(self):
        try:
            (photo,) = self.photos.all()[4:5]
            return photo.file.url
        except ValueError:
            return None

    def get_calendars(self):
        now = timezone.now()
        this_year = now.year
        this_month = now.month
        next_month = this_month + 1
        if this_month == 12:
            next_month = 1
        this_month_cal = Calendar(this_year, this_month)
        next_month_cal = Calendar(this_year, next_month)
        return [this_month_cal, next_month_cal]

    class Meta:
        verbose_name = "숙소"
        verbose_name_plural = "숙소"
