from django.db import models
from django.utils import timezone
from core import models as core_models


class Conversation(core_models.TimeStampedModel):

    """ Conversation Model Definition """

    participants = models.ManyToManyField(
        "users.User", related_name="converstation", blank=True, verbose_name="참가자"
    )

    def __str__(self):
        usernames = []
        for user in self.participants.all():
            usernames.append(user.username)
        return ", ".join(usernames)

    def count_messages(self):
        return self.messages.count()

    count_messages.short_description = "메세지 개수"

    def count_participants(self):
        return self.participants.count()

    count_participants.short_description = "참가자 인원수"

    def get_first_message_date(self):
        try:
            message = self.messages.all().first()
            return message.created
        except ValueError:
            return None

    def get_last_message_date(self):
        try:
            message = self.messages.all().last()
            return message.created
        except ValueError:
            return None

    def get_reverse_second_message_date(self):
        try:
            count_message = self.messages.count()
            (message,) = self.messages.all()[count_message - 2 : count_message - 1]
            return message.created
        except ValueError:
            return None

    def check_day_changed(self):
        try:
            count_message = self.messages.count()
            (message1,) = self.messages.all()[count_message - 2 : count_message - 1]
            message2 = self.messages.all().last()
            if message2.created.day - message1.created.day >= 1:
                return True
            else:
                return False
        except ValueError:
            return None

    class Meta:

        verbose_name = "대화방"
        verbose_name_plural = "대화방"


class Message(core_models.TimeStampedModel):

    """ Message Model Definition """

    message = models.TextField(verbose_name="메세지")
    user = models.ForeignKey(
        "users.User",
        related_name="messages",
        on_delete=models.CASCADE,
        verbose_name="사용자",
    )
    conversation = models.ForeignKey(
        "Conversation",
        related_name="messages",
        on_delete=models.CASCADE,
        verbose_name="대화방",
    )

    def __str__(self):
        return f"{self.user} 대화: {self.message}"

    class Meta:

        verbose_name = "메세지"
        verbose_name_plural = "메세지"
