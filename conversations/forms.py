from django import forms
from django.utils.translation import gettext_lazy as _


class AddMessageForm(forms.Form):

    message = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"placeholder": _("메세지 입력")})
    )
