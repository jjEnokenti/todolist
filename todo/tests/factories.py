import factory
from django.contrib.auth import get_user_model
from goals import models


USER_MODEL = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = USER_MODEL

    username = factory.Sequence(lambda n: f'test_user_{n}')
    password = 'password'
    email = factory.Sequence(lambda n: f'test{n}@example.com')


class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Board

    title = factory.Sequence(lambda n: f'test board {n}')


class BoardParticipantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.BoardParticipant

    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)
    role = models.BoardParticipant.Role.owner


class GoalCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.GoalCategory

    title = factory.Sequence(lambda n: f'test category {n}')
    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)


class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Goal

    title = factory.Sequence(lambda n: f'test goal {n}')
    category = factory.SubFactory(GoalCategoryFactory)


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Comment

    user = factory.SubFactory(UserFactory)
    goal = factory.SubFactory(GoalFactory)
    text = factory.faker.Faker('name')
