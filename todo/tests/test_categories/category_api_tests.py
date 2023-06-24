import pytest
from goals.models import BoardParticipant
from goals.serializers.category import GoalCategorySerializer
from rest_framework import status
from rest_framework.reverse import reverse


@pytest.fixture
def create_category_for_test_writer(user, board_factory, goal_category_factory,
                                    board_participant_factory
                                    ):
    board = board_factory.create()
    board_participant_factory.create(board=board, user=user, role=BoardParticipant.Role.writer)

    return goal_category_factory.create(board=board)


@pytest.fixture
def create_category_for_test_reader(user, board_factory, goal_category_factory,
                                    board_participant_factory
                                    ):
    board = board_factory.create()
    board_participant_factory.create(board=board, user=user, role=BoardParticipant.Role.reader)

    return goal_category_factory.create(board=board)


@pytest.mark.django_db
class TestCategoryAPI:
    def test_is_anon_permissions_get_list_categories(self, client):
        url = reverse('list_goal_category')

        response = client.get(path=url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_is_anon_permissions_create_category(self, client, board):
        url = reverse('create_goal_category')

        payload = {
            'title': 'this category never be created',
            'board': board.pk
        }

        response = client.get(path=url, data=payload)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_is_anon_permissions_get_single_category(self, client, goal_category):
        url = reverse('detail_goal_category', kwargs={'pk': goal_category.pk})

        response = client.get(path=url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_is_anon_permissions_update_category(self, client, goal_category):
        url = reverse('detail_goal_category', kwargs={'pk': goal_category.pk})

        payload = {
            'title': 'this category never be updated',
        }

        response = client.patch(path=url, data=payload, content_type='application/json')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_is_anon_permissions_delete_category(self, client, goal_category):
        url = reverse('detail_goal_category', kwargs={'pk': goal_category.pk})

        response = client.delete(path=url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_category_as_owner(self, auth_client, board, board_participant):
        url = reverse('create_goal_category')

        title = 'new test category'
        payload = {
            'title': title,
            'board': board.pk
        }

        response = auth_client.post(path=url, data=payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['board'] == board.pk
        assert response.data['title'] == title

    def test_create_category_as_writer(self, auth_client, create_category_for_test_writer):
        category = create_category_for_test_writer
        url = reverse('create_goal_category')

        title = 'new test category as writer'
        payload = {
            'title': title,
            'board': category.board.pk,
        }

        response = auth_client.post(path=url, data=payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['board'] == category.board.pk
        assert response.data['title'] == title

    def test_create_category_as_reader(self, auth_client, create_category_for_test_reader):
        category = create_category_for_test_reader
        url = reverse('create_goal_category')

        title = 'this category never be created'
        payload = {
            'title': title,
            'board': category.board.pk,
        }

        response = auth_client.post(path=url, data=payload)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_single_category_as_owner(self, auth_client, goal_category, board_participant):
        url = reverse('detail_goal_category', kwargs={'pk': goal_category.pk})

        response = auth_client.get(path=url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == goal_category.pk
        assert response.data['title'] == goal_category.title

    def test_get_single_category_as_writer(self, auth_client, create_category_for_test_writer):
        category = create_category_for_test_writer
        url = reverse('detail_goal_category', kwargs={'pk': category.pk})

        response = auth_client.get(path=url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == category.title
        assert response.data['board'] == category.board.pk

    def test_get_single_category_as_reader(self, auth_client, create_category_for_test_reader):
        category = create_category_for_test_reader
        url = reverse('detail_goal_category', kwargs={'pk': category.pk})

        response = auth_client.get(path=url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == category.title
        assert response.data['board'] == category.board.pk

    def test_get_list_category_as_owner(self, auth_client, board, goal_category_factory, board_participant):
        url = reverse('list_goal_category')
        count = 3
        categories = goal_category_factory.create_batch(size=count, board=board)

        response = auth_client.get(path=url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == GoalCategorySerializer(categories, many=True).data
        assert len(response.data) == count

    def test_get_list_category_as_writer(self, auth_client, create_category_for_test_writer):
        url = reverse('list_goal_category')

        response = auth_client.get(path=url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == GoalCategorySerializer([create_category_for_test_writer], many=True).data
        assert len(response.data) == 1

    def test_get_list_category_as_reader(self, auth_client, create_category_for_test_reader):
        url = reverse('list_goal_category')

        response = auth_client.get(path=url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == GoalCategorySerializer([create_category_for_test_reader], many=True).data
        assert len(response.data) == 1

    def test_update_category_as_owner(self, auth_client, board_participant, goal_category):
        url = reverse('detail_goal_category', kwargs={'pk': goal_category.pk})
        update_data = {
            'title': 'update title',
        }

        response = auth_client.patch(path=url, data=update_data, content_type='application/json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] != goal_category.title

    def test_update_category_as_writer(self, auth_client, create_category_for_test_writer):
        category = create_category_for_test_writer
        url = reverse('detail_goal_category', kwargs={'pk': category.pk})

        update_data = {
            'title': 'writer can update this title',
        }

        response = auth_client.patch(path=url, data=update_data, content_type='application/json')
        category_response = auth_client.get(path=url)

        assert response.status_code == status.HTTP_200_OK
        assert category_response.data['title'] == 'writer can update this title'

    def test_update_category_as_reader(self, auth_client, create_category_for_test_reader):
        category = create_category_for_test_reader
        url = reverse('detail_goal_category', kwargs={'pk': category.pk})

        update_data = {
            'title': 'reader cant update this title',
        }

        response = auth_client.patch(path=url, data=update_data, content_type='application/json')
        category_response = auth_client.get(path=url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert category_response.data['title'] != 'reader cant update this title'

    def test_delete_category_as_owner(self, auth_client, board_participant, goal_category):
        url = reverse('detail_goal_category', kwargs={'pk': goal_category.pk})

        response = auth_client.delete(path=url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_category_as_writer(self, auth_client, create_category_for_test_writer):
        category = create_category_for_test_writer
        url = reverse('detail_goal_category', kwargs={'pk': category.pk})

        response = auth_client.delete(path=url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_category_as_reader(self, auth_client, create_category_for_test_reader):
        category = create_category_for_test_reader
        url = reverse('detail_goal_category', kwargs={'pk': category.pk})

        response = auth_client.delete(path=url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
