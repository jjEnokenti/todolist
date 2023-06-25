from pytest_factoryboy import register
from tests import factories


pytest_plugins = 'tests.fixtures'


register(factories.UserFactory)
register(factories.BoardFactory)
register(factories.BoardParticipantFactory)
register(factories.GoalCategoryFactory)
register(factories.GoalFactory)
register(factories.CommentFactory)
