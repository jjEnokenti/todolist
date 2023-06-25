import pytest
from goals.models import BoardParticipant
from tests import factories


@pytest.fixture
def auth_client(client, user):
    client.force_login(user)
    return client


@pytest.fixture
def password():
    return factories.TEST_USER_PASSWORD


@pytest.fixture
def create_goal_for_test_writer(user, board_factory, goal_category_factory,
                                board_participant_factory, goal_factory
                                ):
    board = board_factory.create()
    board_participant_factory.create(board=board, user=user, role=BoardParticipant.Role.writer)
    category = goal_category_factory.create(board=board)

    return goal_factory.create(category=category)


@pytest.fixture
def create_goal_for_test_reader(user, board_factory, goal_category_factory,
                                board_participant_factory, goal_factory
                                ):
    board = board_factory.create()
    board_participant_factory.create(board=board, user=user, role=BoardParticipant.Role.reader)
    category = goal_category_factory.create(board=board)

    return goal_factory.create(category=category)
