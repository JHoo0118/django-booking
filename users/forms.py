from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "이메일", "autocomplete": "off"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호", "autocomplete": "off"})
    )

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("잘못된 비밀번호입니다."))

        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("계정이 존재하지 않습니다."))


class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("first_name", "email")
        widgets = {
            "first_name": forms.TextInput(
                attrs={"placeholder": _("이름"), "autocomplete": "off"}
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": _("이메일"), "autocomplete": "off"}
            ),
        }

    password = forms.CharField(
        label="비밀번호",
        widget=forms.PasswordInput(
            attrs={"placeholder": _("비밀번호"), "autocomplete": "off"}
        ),
    )
    password1 = forms.CharField(
        label="비밀번호 확인",
        widget=forms.PasswordInput(
            attrs={"placeholder": _("비밀번호 확인"), "autocomplete": "off"}
        ),
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError("이미 사용중인 이메일입니다.", code="existing_user")
        except models.User.DoesNotExist:
            return email

    def clean_password1(self):
        min_length = 8
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        print(self.cleaned_data)
        print(password, password1)
        if len(password) < min_length:
            raise forms.ValidationError("비밀번호를 최소 8자리 이상으로 해주세요.")
        if password != password1:
            raise forms.ValidationError("비밀번호가 서로 다릅니다.")
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("최소 1자리 이상의 숫자를 포함해주세요.")
        if not any(char.isalpha() for char in password):
            raise forms.ValidationError("최소 1자리 이상의 알파벳을 포함해주세요.")

        return password

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)
        user.save()
