import os

from aiogram.types import (
    Message,
    Update
)
from bot.models import TgUser
from bot.tg.client import TgClient
from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from goals.models import (
    Board,
    BoardParticipant,
    Goal,
    GoalCategory
)


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
        if not goals:
            return self.send_message(chat_id=message.chat.id, text='У вас пока еще нет целей.')
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

    def input_data(self, message: Message, text: str):
        while True:
            self.tg_client.send_message(
                message.chat.id,
                text=text)
            temp = self.tg_client.get_updates(offset=self.offset)
            if temp.result:
                new: Update = temp.result[0]
                self.offset = new.update_id + 1
                return new

    def get_category(self, message: Message, tg_user: TgUser):
        categories = GoalCategory.objects.filter(
            board__participants__user=tg_user.user,
            is_deleted=False
        )
        if not categories:
            board = Board.objects.filter(
                participants__user=tg_user.user,
                participants__role=BoardParticipant.Role.owner).first()
            if not board:
                board = Board.objects.create(title='Мои цели')
                BoardParticipant.objects.create(board=board, user=tg_user.user, role=BoardParticipant.Role.owner)
            categories = [GoalCategory.objects.create(title='Новая категория', user=tg_user.user, board=board)]

        user_categories = [f'{cat.title}: {cat.id}' for cat in categories]

        format_categories = '\n'.join(user_categories)
        text = f'Выберите категорию из списка \n{format_categories} \nи отправь ее номер в ответном сообщении'
        category = self.input_data(message, text).message.text
        if category == '/cancel':
            return self.cancel(chat_id=message.chat.id)
        elif category not in format_categories:
            return self.send_message(chat_id=message.chat.id, text='Такой категории не существует.')

        return category

    def cancel(self, chat_id):
        self.send_message(chat_id=chat_id, text='Операция отменена.')

    def goal_create(self, message: Message, tg_user: TgUser):
        while True:

            category = self.get_category(message, tg_user)
            if category is None:
                break
            goal_title = self.input_data(message, text='Введите названия своей цели').message.text
            if goal_title == '/cancel':
                return self.cancel(chat_id=message.chat.id)

            new_goal = Goal.objects.create(
                category_id=category,
                title=goal_title
            )
            if new_goal:
                text = '\n'.join(
                    (f'Название - {new_goal.title}',
                     f'Описание - {new_goal.description or "Blank"}',
                     f'Категория - {new_goal.category.title}',
                     f'Статус - {new_goal.get_status_display()}',
                     f'Приоритет - {new_goal.get_priority_display()}',
                     f'Дата дедлайна - {new_goal.due_date or "Indefinite"}',
                     f'Дата создания - {new_goal.created}',
                     f'Дата обновления - {new_goal.updated}'))
                return self.send_message(chat_id=message.chat.id, text=text)
            self.send_message(message.chat.id, text='Не удалось создать цель, попробуйте еще раз.')
