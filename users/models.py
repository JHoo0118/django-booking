import uuid
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.shortcuts import reverse
from django.template.loader import render_to_string
from core import managers as core_managers


class User(AbstractUser):

    """ Custom User Model """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, _("남자")),
        (GENDER_FEMALE, _("여자")),
        (GENDER_OTHER, _("그 외")),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "kr"

    LANGUAGE_CHOICES = ((LANGUAGE_ENGLISH, _("영어")), (LANGUAGE_KOREAN, _("한국어")))

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"

    CURRENCY_CHOICES = ((CURRENCY_USD, "USD"), (CURRENCY_KRW, "KRW"))

    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGIN_KAKAO = "kakao"
    LOGIN_NAVER = "naver"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, _("이메일")),
        (LOGIN_GITHUB, _("깃허브")),
        (LOGIN_KAKAO, _("카카오")),
        (LOGIN_NAVER, _("네이버")),
    )
    avatar = models.ImageField(_("프로필 사진"), upload_to="avatars", blank=True)
    gender = models.CharField(
        _("성별"), choices=GENDER_CHOICES, max_length=10, blank=True
    )
    bio = models.TextField(_("자기소개"), max_length=200, blank=True)
    birthdate = models.DateField(_("생일"), blank=True, null=True)
    language = models.CharField(
        _("언어"),
        choices=LANGUAGE_CHOICES,
        max_length=2,
        blank=True,
        default=LANGUAGE_KOREAN,
    )
    currency = models.CharField(
        _("통화"),
        choices=CURRENCY_CHOICES,
        max_length=3,
        blank=True,
        default=CURRENCY_KRW,
    )
    superhost = models.BooleanField(_("슈퍼호스트"), default=False)
    email_verified = models.BooleanField(_("이메일 인증"), default=False)
    email_secret = models.CharField(_("보안 코드"), max_length=20, default="", blank=True)
    login_method = models.CharField(
        _("로그인 방법"), max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL
    )

    objects = core_managers.CustomUserManager()

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})

    def verify_email(self):
        if self.email_verified is False:
            secret = uuid.uuid4().hex[:20]
            self.email_secret = secret
            html_message = render_to_string(
                "emails/verify_email.html", {"secret": secret}
            )
            send_mail(
                _("계정 인증"),
                strip_tags(html_message),
                settings.EMAIL_FROM,
                [self.email],
                fail_silently=False,
                html_message=html_message,
            )
            self.save()
        return
