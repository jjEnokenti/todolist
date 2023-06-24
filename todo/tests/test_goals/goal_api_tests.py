import pytest
from goals import models
from goals.serializers.goal import GoalSerializer
from rest_framework import status
from rest_framework.reverse import reverse


@pytest.mark.django_db
class TestGoalAPI:

    def test_is_anon_permissions_get_list_goals(self, client):
        url = reverse('list_goal')

        response = client.get(path=url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_is_anon_permissions_create_goal(self, client, goal_category):
        url = reverse('create_goal')

        payload = {
            'title': 'this goal never be created',
            'category': goal_category.pk
        }

        response = client.get(path=url, data=payload)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_is_anon_permissions_get_single_goal(self, client, goal):
        url = reverse('detail_goal', kwargs={'pk': goal.pk})

        response = client.get(path=url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_is_anon_permissions_update_goal(self, client, goal):
        url = reverse('detail_goal', kwargs={'pk': goal.pk})

        payload = {
            'title': 'this goal never be updated',
        }

        response = client.patch(path=url, data=payload, content_type='application/json')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_is_anon_permissions_delete_goal(self, client, goal):
        url = reverse('detail_goal', kwargs={'pk': goal.pk})

        response = client.delete(path=url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_goal_as_owner(self, auth_client, board_participant, goal_category):
        url = reverse('create_goal')
        payload = {
            'title': 'new test goal',
            'category': goal_category.pk,
        }

        response = auth_client.post(path=url, data=payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['category'] == goal_category.pk
        assert response.data['title'] == 'new test goal'

    def test_create_goal_as_writer(self, auth_client, create_goal_for_test_writer):
        goal = create_goal_for_test_writer
        url = reverse('create_goal')
        payload = {
            'title': 'new test goal as writer',
            'category': goal.category.pk,
        }

        response = auth_client.post(path=url, data=payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['category'] == goal.category.pk
        assert response.data['title'] == 'new test goal as writer'

    def test_create_goal_as_reader(self, auth_client, create_goal_for_test_reader):
        goal = create_goal_for_test_reader
        url = reverse('create_goal')
        payload = {
            'title': 'new test goal newer be created',
            'category': goal.category.pk,
        }

        response = auth_client.post(path=url, data=payload)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_single_goal_as_owner(self, auth_client, board_participant, goal, goal_category):
        url = reverse('detail_goal', kwargs={'pk': goal.pk})

        response = auth_client.get(path=url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == goal.title
        assert response.data['category'] == goal_category.pk

    def test_get_single_goal_as_writer(self, auth_client, create_goal_for_test_writer):
        goal = create_goal_for_test_writer
        url = reverse('detail_goal', kwargs={'pk': goal.pk})

        response = auth_client.get(path=url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == goal.title
        assert response.data['category'] == goal.category.pk

    def test_get_single_goal_as_reader(self, auth_client, create_goal_for_test_reader):
        goal = create_goal_for_test_reader
        url = reverse('detail_goal', kwargs={'pk': goal.pk})

        response = auth_client.get(path=url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == goal.title
        assert response.data['category'] == goal.category.pk

    def test_get_list_goal_as_owner(self, auth_client, board_participant, goal_factory, goal_category):
        url = reverse('list_goal')
        count = 5
        goals = goal_factory.create_batch(size=count, category=goal_category)

        response = auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == GoalSerializer(goals, many=True).data
        assert len(response.data) == count

    def test_get_list_goal_as_writer(self, auth_client, create_goal_for_test_writer):
        url = reverse('list_goal')

        response = auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == GoalSerializer([create_goal_for_test_writer], many=True).data
        assert len(response.data) == 1

    def test_get_list_goal_as_reader(self, auth_client, create_goal_for_test_reader):
        url = reverse('list_goal')

        response = auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == GoalSerializer([create_goal_for_test_reader], many=True).data
        assert len(response.data) == 1

    def test_update_goal_as_owner(self, auth_client, board_participant, goal):
        url = reverse('detail_goal', kwargs={'pk': goal.pk})
        update_data = {
            'title': 'update title',
            'status': models.Goal.Status.done,
        }

        response = auth_client.patch(path=url, data=update_data, content_type='application/json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] != goal.title
        assert response.data['status'] == models.Goal.Status.done

    def test_update_goal_as_writer(self, auth_client, create_goal_for_test_writer):
        goal = create_goal_for_test_writer
        url = reverse('detail_goal', kwargs={'pk': goal.pk})

        update_data = {
            'title': 'writer can update this title',
        }

        response = auth_client.patch(path=url, data=update_data, content_type='application/json')
        goal_response = auth_client.get(path=url)

        assert response.status_code == status.HTTP_200_OK
        assert goal_response.data['title'] == 'writer can update this title'

    def test_update_goal_as_reader(self, auth_client, create_goal_for_test_reader):
        goal = create_goal_for_test_reader
        url = reverse('detail_goal', kwargs={'pk': goal.pk})

        update_data = {
            'title': 'reader cant update this title',
        }

        response = auth_client.patch(path=url, data=update_data, content_type='application/json')
        goal_response = auth_client.get(path=url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert goal_response.data['title'] != 'reader cant update this title'

    def test_try_update_goal_category(self, auth_client, board_participant, goal, goal_category_factory):
        url = reverse('detail_goal', kwargs={'pk': goal.pk})

        category = goal_category_factory.create()
        update_data = {
            'category': category.pk,
        }

        response = auth_client.patch(path=url, data=update_data, content_type='application/json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['category'] != category.pk
        assert response.data['category'] == goal.category.pk

    def test_delete_goal_as_owner(self, auth_client, board_participant, goal):
        url = reverse('detail_goal', kwargs={'pk': goal.pk})

        response = auth_client.delete(path=url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_goal_as_writer(self, auth_client, create_goal_for_test_writer):
        goal = create_goal_for_test_writer
        url = reverse('detail_goal', kwargs={'pk': goal.pk})

        response = auth_client.delete(path=url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_goal_as_reader(self, auth_client, create_goal_for_test_reader):
        goal = create_goal_for_test_reader
        url = reverse('detail_goal', kwargs={'pk': goal.pk})

        response = auth_client.delete(path=url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
