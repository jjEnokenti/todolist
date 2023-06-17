import uuid

from django.db import models


class TgUser(models.Model):

    user = models.ForeignKey('core.User', verbose_name='Пользователь', null=True, on_delete=models.CASCADE)
    chat_id = models.PositiveBigIntegerField(verbose_name='ID телеграм чата')
    tg_user_id = models.BigIntegerField(verbose_name='ID Телеграм пользователя')
    tg_username = models.CharField(verbose_name='Никнейм в Телеграм')
    verification_code = models.CharField(verbose_name='Верификационный код', max_length=36, null=True)

    class Meta:
        verbose_name = 'Телеграм пользователь'
        verbose_name_plural = 'Телеграм пользователи'

    def __str__(self):
        return self.user.username

    def generate_code(self):
        code = uuid.uuid4()
        self.verification_code = code
        self.save()
        return code

    # def get_absolute_url(self):
    #     return reverse('bot-verify', kwargs={'slug': self.verification_code})
