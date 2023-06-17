import os

from aiogram.types import Message
from bot.models import TgUser
from bot.tg.client import TgClient
from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from goals.models import Goal


load_dotenv()


class Command(BaseCommand):
    help = 'Run echo bot command'

    tg_client = TgClient(os.getenv('BOT_TOKEN'))
    offset = 0

    def handle(self, *args, **options):

        while True:
            result = self.tg_client.get_updates(offset=self.offset)
            for item in result.result:
                self.offset = item.update_id + 1
                print(item.message)
                self.handle_message(item.message)

    def handle_message(self, message: Message):
        user = message.from_user

        tg_user, created = TgUser.objects.get_or_create(
            tg_username=user.username or user.full_name,
            tg_user_id=user.id,
            chat_id=message.chat.id
        )
        if message.text == '/start':
            if created:
                self.send_message(chat_id=message.chat.id, text=f'Привет {tg_user.tg_username}')
            else:
                self.send_message(chat_id=message.chat.id, text='Уже был')
        else:
            if not tg_user.verification_code or not tg_user.user:
                if tg_user.verification_code:
                    code = tg_user.verification_code
                else:
                    code = tg_user.generate_code()
                text = f'Необходимо верифицировать бота на сайте.\n{code} введите этот код на сайте'
                self.send_message(chat_id=message.chat.id, text=text)

            elif message.text == '/goals':
                self.get_goals(message=message, tg_user=tg_user)

            elif message.text == '/create':
                self.goal_create(message, tg_user)
            else:
                self.send_message(message.chat.id, text='Неизвестная команда.')

    def send_message(self, chat_id, text: str):
        self.tg_client.send_message(chat_id=chat_id, text=text)

    def get_goals(self, message: Message, tg_user: TgUser):

        goals = Goal.objects.filter(category__board__participants__user=tg_user.user).exclude(
            status=Goal.Status.archived
        )
        text = '\n----------\n'.join(['\n'.join((
            f'Название - {goal.title}',
            f'Описание - {goal.description or "Blank"}',
            f'Категория - {goal.category.title}',
            f'Статус - {goal.get_status_display()}',
            f'Приоритет - {goal.get_priority_display()}',
            f'Дата дедлайна - {goal.due_date or "Indefinite"}',
            f'Дата создания - {goal.created}',
            f'Дата обновления - {goal.updated}',
        )) for goal in goals])

        self.send_message(chat_id=message.chat.id, text=text)
