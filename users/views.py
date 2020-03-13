import os
import requests
import uuid
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from . import forms, models, mixins


class LoginView(mixins.LoggedOutOnlyView, FormView):
    template_name = "users/login.html"
    form_class = forms.LoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, _("로그인에 성공하였습니다."))
        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:home")


def log_out(request):
    messages.success(request, _("성공적으로 로그아웃 되었습니다."))
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(mixins.LoggedOutOnlyView, FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, _("로그인에 성공하였습니다."))
        # user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
    except models.user.DoesNotExist:
        pass

    return redirect(reverse("core:home"))


def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://django-booking.eba-a3mcndmb.ap-northeast-2.elasticbeanstalk.com/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        code = request.GET.get("code", None)
        if code is not None:
            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            token_json = token_request.json()
            error = token_json.get("error", None)
            if error is not None:
                raise GithubException("토큰을 가져오지 못하였습니다.")
            else:
                access_token = token_json.get("access_token")
                profile_request = requests.get(
                    f"https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                profile_json = profile_request.json()
                username = profile_json.get("login", None)
                if username is not None:
                    name = profile_json.get("name")
                    email = profile_json.get("email")
                    bio = profile_json.get("bio")
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException("이미 가입된 이메일 주소입니다.")
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            email=email,
                            first_name=name,
                            username=email,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                            email_verified=True,
                        )
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    messages.success(request, _("로그인에 성공하였습니다."))
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException("프로필을 얻을 수 없습니다.")
        else:
            raise GithubException("코드를 얻을 수 없습니다.")
    except GithubException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class KakaoException(Exception):
    pass


def kakao_login(request):
    client_id = os.environ.get("KAKAO_ID")
    redirect_uri = "http://django-booking.eba-a3mcndmb.ap-northeast-2.elasticbeanstalk.com/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )


def kakao_callback(request):
    try:
        code = request.GET.get("code")
        client_id = os.environ.get("KAKAO_ID")
        redirect_uri = "http://django-booking.eba-a3mcndmb.ap-northeast-2.elasticbeanstalk.com/users/login/kakao/callback"
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )
        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoException("코드를 얻을 수 없습니다.")
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        kakao_account = profile_json.get("kakao_account")
        email = kakao_account.get("email", None)
        if email is None:
            raise KakaoException("로그인을 위한 이메일을 제공해주세요.")
        profile = kakao_account.get("profile")
        nickname = profile.get("nickname")
        profile_image = profile.get("profile_image_url")
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                raise KakaoException("이미 가입된 이메일 주소입니다.")
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                login_method=models.User.LOGIN_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()
            if profile_image is not None:
                photo_request = requests.get(profile_image)
                user.avatar.save(
                    f"{nickname}-avatar", ContentFile(photo_request.content)
                )
        login(request, user)
        messages.success(request, _("로그인에 성공하였습니다."))
        return redirect(reverse("core:home"))
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class NaverException(Exception):
    pass


def naver_login(request):
    client_id = os.environ.get("NAVER_ID")
    state = uuid.uuid4().hex[:16]
    redirect_uri = "http://django-booking.eba-a3mcndmb.ap-northeast-2.elasticbeanstalk.com/users/login/naver/callback"
    return redirect(
        f"https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&state={state}"
    )


def naver_callback(request):
    try:
        code = request.GET.get("code")
        state = request.GET.get("state")
        client_id = os.environ.get("NAVER_ID")
        client_secret = os.environ.get("NAVER_SECRET")
        redirect_uri = "http://django-booking.eba-a3mcndmb.ap-northeast-2.elasticbeanstalk.com/users/login/naver/callback"
        token_request = requests.get(
            f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&code={code}&state={state}"
        )
        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:
            raise NaverException("코드를 얻을 수 없습니다.")

        access_token = token_json.get("access_token")
        refresh_token = token_json.get("refresh_token")
        print(access_token)
        profile_request = requests.get(
            "https://openapi.naver.com/v1/nid/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        response = profile_json.get("response")
        email = response.get("email")
        name = response.get("name")
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_NAVER:
                raise NaverException("이미 가입된 이메일 주소입니다.")
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                username=email,
                first_name=name,
                login_method=models.User.LOGIN_NAVER,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()
        login(request, user)
        messages.success(request, _("로그인에 성공하였습니다."))
        return redirect(reverse("core:home"))

    except NaverException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


# class GoogleException:
#     pass


# def google_login(request):
#     client_id = os.environ.get("GOOGLE_ID")
#     state = uuid.uuid4().hex[:30]
#     redirect_uri = "http://127.0.0.1:8000/users/login/google/callback"
#     scope = "openid%20profile%20email"
#     return redirect(
#         f"https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id={client_id}&scope={scope}&redirect_uri={redirect_uri}&state={state}"
#     )


# def google_callback(request):
#     code = request.GET.get("code")
#     client_id = os.environ.get("GOOGLE_ID")
#     client_secret = os.environ.get("GOOGLE_SECRET")
#     redirect_uri = "http://127.0.0.1:8000/users/login/google/callback"
#     token_request = requests.get(
#         f"https://oauth2.googleapis.com/token?grant_type=authorization_code&code={code}&client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}"
#     )
#     token_json = token_request.json()
#     print(token_json)
# error = token_json.get("error", None)
# if error is not None:
#     raise GoogleException()
# access_token = token_json.get("access_token")
# print(access_token)


class UserProfileView(DetailView):

    model = models.User
    context_object_name = "user_obj"


class UpdateProfileView(mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = models.User
    template_name = "users/update-profile.html"
    context_object_name = "user_obj"

    fields = (
        "first_name",
        "avatar",
        "gender",
        "bio",
        "birthdate",
        "language",
        "currency",
    )

    success_message = _("프로필이 업데이트 되었습니다.")

    def get_object(self, queryset=None):
        # 수정하고 싶은 유저 반환
        return self.request.user

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        form = super(UpdateProfileView, self).get_form(form_class)

        form.fields["first_name"].widget.attrs = {
            "autocomplete": "off",
        }
        form.fields["bio"].widget.attrs = {
            "autocomplete": "off",
        }
        form.fields["birthdate"].widget.attrs = {
            "placeholder": "(1995-01-18)",
            "autocomplete": "off",
        }
        return form

    # 이메일 변경
    # def form_valid(self, form):
    #     email = form.cleaned_data.get("email")
    #     self.object.username = email
    #     self.object.save()
    #     return super().form_valid(form)


class UpdatePasswordView(
    mixins.LoggedInOnlyView,
    mixins.EmailLoginOnlyView,
    SuccessMessageMixin,
    PasswordChangeView,
):

    template_name = "users/update-password.html"
    success_message = _("비밀번호가 변경되었습니다.")

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        return form

    def get_success_url(self):
        return self.request.user.get_absolute_url()


def switch_language(request):
    lang = request.GET.get("lang", None)
    if lang is not None:
        request.session[translation.LANGUAGE_SESSION_KEY] = lang
    return HttpResponse(status=200)
