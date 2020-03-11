from django import forms
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from . import models


class SearchForm(forms.Form):
    city = forms.CharField(label=_("도시"), initial="모든 곳")
    country = CountryField(default="KR").formfield()
    price = forms.IntegerField(label=_("가격"), required=False)
    room_type = forms.ModelChoiceField(
        label=_("숙소 유형"),
        required=False,
        empty_label="모든 숙소 유형",
        queryset=models.RoomType.objects.all(),
    )
    guests = forms.IntegerField(
        label=_("게스트"), required=False, min_value=1, max_value=9
    )
    bedrooms = forms.IntegerField(
        label=_("침실"), required=False, min_value=1, max_value=9
    )
    beds = forms.IntegerField(label=_("침대"), required=False, min_value=1, max_value=9)
    baths = forms.IntegerField(label=_("욕실"), required=False, min_value=1, max_value=9)
    instant_book = forms.BooleanField(label=_("즉시예약"), required=False)
    superhost = forms.BooleanField(label=_("슈퍼호스트"), required=False)
    amenities = forms.ModelMultipleChoiceField(
        label=_("편의시설"),
        required=False,
        queryset=models.Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    facilities = forms.ModelMultipleChoiceField(
        label=_("시설"),
        required=False,
        queryset=models.Facility.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )


class CreatePhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ("caption", "file")

        widgets = {
            "caption": forms.TextInput(attrs={"autocomplete": "off"}),
        }

    def save(self, pk, *args, **kwargs):
        photo = super().save(commit=False)
        room = models.Room.objects.get(pk=pk)
        photo.room = room
        photo.save()


class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = models.Room
        fields = (
            "name",
            "description",
            "country",
            "city",
            "price",
            "address",
            "guests",
            "beds",
            "bedrooms",
            "baths",
            "check_in",
            "check_out",
            "instant_book",
            "room_type",
            "amenities",
            "facilities",
            "house_rules",
        )

        widgets = {
            "name": forms.TextInput(attrs={"autocomplete": "off"}),
            "city": forms.TextInput(attrs={"autocomplete": "off"}),
            "address": forms.TextInput(attrs={"autocomplete": "off"}),
            "check_in": forms.TextInput(
                attrs={"placeholder": "17:12:34", "autocomplete": "off"}
            ),
            "check_out": forms.TextInput(
                attrs={"placeholder": "17:12:34", "autocomplete": "off"}
            ),
        }

    def save(self, *args, **kwargs):
        room = super().save(commit=False)
        return room
