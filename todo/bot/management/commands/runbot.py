import time

from bot.custom_exceptions import CategoryNotFound
from bot.tg.client import TgClient
from bot.tg.controller import Controller
from bot.tg.dc import Message
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import QuerySet
from goals.models import GoalCategory


class Command(BaseCommand):
    """Hande message class."""
    help = 'Run bot command'

    tg_client = TgClient(settings.BOT_TOKEN)
    offset = 0

    def handle(self, *args, **options):

        while True:
            time.sleep(0.05)
            result = self.tg_client.get_updates(offset=self.offset)
            for item in result.result:
                self.offset = item.update_id + 1
                if not item or not item.message:
                    continue
                self.handle_message(item.message)

    def send_message(self, chat_id, text: str):
        self.tg_client.send_message(chat_id=chat_id, text=text)

    def user_answer(self, message: Message, text: str) -> str:
        while True:
            self.tg_client.send_message(
                message.chat.id,
                text=text)
            temp = self.tg_client.get_updates(offset=self.offset)
            for item in temp.result:
                self.offset = item.update_id + 1
                if not item or not item.message:
                    continue
                return item.message.text

    def handle_message(self, message: Message):
        controller = Controller(
            message=message
        )

        if message.text not in controller.allowed_commands:
            self.send_message(message.chat.id, text='Неизвестная команда.')

        elif message.text == '/cancel':
            self.send_message(message.chat.id, 'Нет открытых операций для отмены.')

        elif message.text == '/start':
            if controller.created:
                self.tg_client.send_message(
                    chat_id=message.chat.id,
                    text=f'Привет {controller.tg_user.tg_username}'
                )
            else:
                self.send_message(chat_id=message.chat.id, text='Уже был')

        elif not controller.tg_user.verification_code or not controller.tg_user.user:
            if controller.tg_user.verification_code:
                code = controller.tg_user.verification_code
            else:
                code = controller.tg_user.generate_code()
            text = f'Необходимо верифицировать бота.\n{code} введите этот код на сайте'

            self.send_message(chat_id=message.chat.id, text=text)

        elif message.text == '/goals':
            self.get_goals(message, controller.get_goals())

        elif message.text == '/create':
            self.create_goal(message, controller)

    def get_goals(self, message: Message, goals):

        text = '\n----------\n'.join(['\n'.join((
            f'Название - {goal.title}',
            f'Описание - {goal.description or "Blank"}',
            f'Категория - {goal.category.title}',
            f'Статус - {goal.get_status_display()}',
            f'Приоритет - {goal.get_priority_display()}',
            f'Дата дедлайна - {goal.due_date or "Indefinite"}',
            f'Дата создания - {goal.created.date()}',
            f'Дата обновления - {goal.updated.date()}',
        )) for goal in goals])

        self.send_message(chat_id=message.chat.id, text=text)

    def get_category(self, message: Message,
                     categories: QuerySet[GoalCategory] | None,
                     text: str | None = None) -> str:

        user_categories = [f'{cat.id}: {cat.title}' for cat in categories]

        text = text or 'Выберите номер категории из списка\n' + '\n'.join(user_categories)

        return self.user_answer(message, text)

    def create_goal(self, message: Message, controller: Controller):
        text = None
        categories = controller.get_categories()
        while True:
            category = self.get_category(message, categories, text)
            if category == '/cancel':
                return self.cancel(message)
            try:
                category = int(category)
                if not controller.get_category(category):
                    raise CategoryNotFound
            except (ValueError, TypeError):
                text = 'Категория должна быть числом. Попробуйте еще раз.'
                continue
            except CategoryNotFound as err:
                text = f'{err.message} Выберите из списка.'
                continue
            break

        title = self.user_answer(message, 'Введите название для цели.')
        if title == '/cancel':
            return self.cancel(message)

        new_goal = controller.create_goal(title=title, pk=category)
        return self.get_goals(message, [new_goal])

    def cancel(self, message: Message):
        self.send_message(chat_id=message.chat.id, text='Операция отменена.')
