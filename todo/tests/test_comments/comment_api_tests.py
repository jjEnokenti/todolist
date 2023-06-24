import pytest
from goals.serializers.comment import CommentSerializer
from rest_framework import status
from rest_framework.reverse import reverse


@pytest.mark.django_db
class TestCommentAPI:
    COMMENTS_SIZE = 5

    @pytest.fixture
    def not_own_comment(self, user_factory, comment_factory, goal):
        return comment_factory.create(user=user_factory.create(), goal=goal)

    @pytest.fixture
    def create_comment_for_test_writer(self, create_goal_for_test_writer, comment_factory):
        return comment_factory.create_batch(size=self.COMMENTS_SIZE, goal=create_goal_for_test_writer)

    @pytest.fixture
    def create_comment_for_test_reader(self, create_goal_for_test_reader, comment_factory):
        return comment_factory.create_batch(size=self.COMMENTS_SIZE, goal=create_goal_for_test_reader)

    def test_is_anon_permissions_get_list_comments(self, client):
        url = reverse('list_goal_comment')

        response = client.get(path=url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_is_anon_permissions_create_comment(self, client, goal):
        url = reverse('create_goal_comment')

        payload = {
            'title': 'this comment never be created',
            'goal': goal.pk
        }

        response = client.get(path=url, data=payload)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_is_anon_permissions_get_single_comment(self, client, comment):
        url = reverse('detail_goal_comment', kwargs={'pk': comment.pk})

        response = client.get(path=url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_is_anon_permissions_update_comment(self, client, comment):
        url = reverse('detail_goal_comment', kwargs={'pk': comment.pk})

        payload = {
            'title': 'this comment never be updated',
        }

        response = client.patch(path=url, data=payload, content_type='application/json')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_is_anon_permissions_delete_comment(self, client, comment):
        url = reverse('detail_goal_comment', kwargs={'pk': comment.pk})

        response = client.delete(path=url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_comment_as_goal_owner(self, auth_client, board_participant, goal):
        url = reverse('create_goal_comment')

        payload = {
            'text': 'new test comment',
            'goal': goal.pk,
        }

        response = auth_client.post(path=url, data=payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['goal'] == goal.pk
        assert response.data['text'] == 'new test comment'

    def test_create_comment_as_goal_writer(self, auth_client, create_goal_for_test_writer):
        goal = create_goal_for_test_writer
        url = reverse('create_goal_comment')
        payload = {
            'text': 'new test comment as writer',
            'goal': goal.pk,
        }

        response = auth_client.post(path=url, data=payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['goal'] == goal.pk
        assert response.data['text'] == 'new test comment as writer'

    def test_create_comment_as_goal_reader(self, auth_client, create_goal_for_test_reader):
        goal = create_goal_for_test_reader
        url = reverse('create_goal_comment')
        payload = {
            'text': 'new test comment newer be created',
            'goal': goal.pk,
        }

        response = auth_client.post(path=url, data=payload)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_single_comment_as_owner(self, auth_client, board_participant, goal, comment):
        url = reverse('detail_goal_comment', kwargs={'pk': comment.pk})

        response = auth_client.get(path=url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['text'] == comment.text
        assert response.data['goal'] == goal.pk

    def test_get_single_comment_as_writer(self, auth_client, create_comment_for_test_writer):
        comment = create_comment_for_test_writer[0]
        url = reverse('detail_goal_comment', kwargs={'pk': comment.pk})

        response = auth_client.get(path=url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['text'] == comment.text
        assert response.data['goal'] == comment.goal.pk

    def test_get_single_comment_as_reader(self, auth_client, create_comment_for_test_reader):
        comment = create_comment_for_test_reader[0]
        url = reverse('detail_goal_comment', kwargs={'pk': comment.pk})

        response = auth_client.get(path=url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['text'] == comment.text
        assert response.data['goal'] == comment.goal.pk

    def test_get_list_comment_as_owner(self, auth_client, board_participant, goal, comment_factory):
        url = reverse('list_goal_comment')

        count = 5
        comments = sorted(
            comment_factory.create_batch(size=count, goal=goal),
            key=lambda com: com.created,
            reverse=True
        )

        response = auth_client.get(path=url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == CommentSerializer(comments, many=True).data
        assert len(response.data) == count

    def test_get_list_comment_as_writer(self, auth_client, create_comment_for_test_writer):
        url = reverse('list_goal_comment')

        response = auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == CommentSerializer(
            sorted(
                create_comment_for_test_writer,
                key=lambda com: com.created,
                reverse=True
            ),
            many=True).data
        assert len(response.data) == self.COMMENTS_SIZE

    def test_get_list_comment_as_reader(self, auth_client, create_comment_for_test_reader):
        url = reverse('list_goal_comment')

        response = auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == CommentSerializer(
            sorted(
                create_comment_for_test_reader,
                key=lambda com: com.created,
                reverse=True
            ),
            many=True).data
        assert len(response.data) == self.COMMENTS_SIZE

    def test_update_comment_with_owner(self, auth_client, board_participant, comment):
        url = reverse('detail_goal_comment', kwargs={'pk': comment.pk})
        update_data = {
            'text': 'update text',
        }

        response = auth_client.patch(path=url, data=update_data, content_type='application/json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['text'] != comment.text

    def test_update_not_own_comment(self, auth_client, board_participant, not_own_comment):
        comment = not_own_comment
        url = reverse('detail_goal_comment', kwargs={'pk': comment.pk})

        text = 'you cant update this comment text'
        update_data = {
            'text': text,
        }

        response = auth_client.patch(path=url, data=update_data, content_type='application/json')
        comment_response = auth_client.get(path=url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert comment_response.data['text'] != text

    def test_try_update_goal_and_user_of_comment(self,
                                                 auth_client,
                                                 board_participant,
                                                 goal, user, comment,
                                                 user_factory,
                                                 goal_factory):
        url = reverse('detail_goal_comment', kwargs={'pk': comment.pk})

        new_goal = goal_factory.create()
        new_user = user_factory.create()
        new_text = 'new updated text'

        update_data = {
            'goal': new_goal.pk,
            'user': new_user.pk,
            'text': new_text,
        }

        response = auth_client.patch(path=url, data=update_data, content_type='application/json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['goal'] != new_goal.pk
        assert response.data['goal'] == goal.pk
        assert response.data['user']['id'] == user.pk
        assert response.data['user']['id'] != new_user.pk
        assert response.data['text'] == new_text

    def test_delete_comment_with_owner(self, auth_client,  board_participant, comment):
        url = reverse('detail_goal_comment', kwargs={'pk': comment.pk})

        response = auth_client.delete(path=url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_not_own_comment(self, auth_client, board_participant, not_own_comment):
        comment = not_own_comment
        url = reverse('detail_goal_comment', kwargs={'pk': comment.pk})

        response = auth_client.delete(path=url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
