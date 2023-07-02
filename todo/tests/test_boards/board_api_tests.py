import json

import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from goals.models import BoardParticipant
from goals.serializers.board import BoardListSerializer


@pytest.mark.django_db
class TestBoardAPI:
    """Board API tests."""

    @pytest.fixture
    def create_board_for_test_writer(self, user, board_factory,
                                     board_participant_factory
                                     ):
        """Board to test writer rights."""

        board = board_factory.create()
        board_participant_factory.create(board=board, user=user, role=BoardParticipant.Role.writer)

        return board

    @pytest.fixture
    def create_board_for_test_reader(self, user, board_factory,
                                     board_participant_factory
                                     ):
        """Board to test reader rights."""

        board = board_factory.create()
        board_participant_factory.create(board=board, user=user, role=BoardParticipant.Role.reader)

        return board

    def test_is_anon_permissions_get_list_boards(self, client):
        """Test anonim user permissions to get list boards."""

        url = reverse('list_board')

        response = client.get(path=url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_is_anon_permissions_create_board(self, client):
        """Test anonim user permissions to create board."""

        url = reverse('create_board')

        payload = {
            'title': 'this board never be created',
        }

        response = client.get(path=url, data=payload)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_is_anon_permissions_get_single_board(self, client, board):
        """Test anonim user permissions to get single board."""

        url = reverse('detail_board', kwargs={'pk': board.pk})

        response = client.get(path=url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_is_anon_permissions_update_board(self, client, board):
        """Test anonim user permissions to update board."""

        url = reverse('detail_board', kwargs={'pk': board.pk})

        payload = {
            'title': 'this board never be updated',
        }

        response = client.patch(path=url, data=payload, content_type='application/json')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_is_anon_permissions_delete_board(self, client, board):
        """Test anonim user permissions to delete board."""

        url = reverse('detail_board', kwargs={'pk': board.pk})

        response = client.delete(path=url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_board(self, auth_client):
        """Test success create board."""

        url = reverse('create_board')
        title = 'new test board'
        payload = {
            'title': title,
        }

        response = auth_client.post(path=url, data=payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == title

    def test_participant_created_board(self, auth_client, board_participant, board, user):
        """Board creator role test."""

        assert board_participant.user == user
        assert board_participant.board == board

    def test_get_single_board(self, auth_client, board, board_participant):
        """Test get single board."""

        url = reverse('detail_board', kwargs={'pk': board.pk})

        response = auth_client.get(path=url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == board.pk
        assert response.data['title'] == board.title

    def test_get_list_board(self, auth_client, board, board_participant):
        """Test get list of boards."""

        url = reverse('list_board')

        response = auth_client.get(path=url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == BoardListSerializer([board], many=True).data

    def test_update_board_add_new_user_as_owner(self, auth_client, user_factory, board, board_participant):
        """Test creator can add new user to board."""

        url = reverse('detail_board', kwargs={'pk': board.pk})

        reader = user_factory.create()
        role = BoardParticipant.Role.reader
        update_data = {
            'title': 'new updated',
            'participants': [
                {
                    'user': reader.username,
                    'role': role
                }
            ]
        }

        response = auth_client.patch(path=url, data=json.dumps(update_data), content_type='application/json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] != board.title
        assert response.data['participants'][1]['user'] == reader.username
        assert response.data['participants'][1]['role'] == role

    def test_update_board_as_writer(self, auth_client, user_factory, create_board_for_test_writer):
        """Test writer can change the board."""

        board = create_board_for_test_writer
        url = reverse('detail_board', kwargs={'pk': board.pk})

        title = 'writer cant update this title'
        reader = user_factory.create()
        role = BoardParticipant.Role.reader
        update_data = {
            'title': 'new updated',
            'participants': [
                {
                    'user': reader.username,
                    'role': role
                }
            ]
        }

        response = auth_client.patch(path=url, data=update_data, content_type='application/json')
        board_response = auth_client.get(path=url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert board_response.data['title'] != title
        assert len(board_response.data['participants']) == 1

    def test_update_board_as_reader(self, auth_client, create_board_for_test_reader):
        """Test reader can change the board."""

        board = create_board_for_test_reader
        url = reverse('detail_board', kwargs={'pk': board.pk})

        title = 'reader cant update this title'
        update_data = {
            'title': title,
        }

        response = auth_client.patch(path=url, data=update_data, content_type='application/json')
        board_response = auth_client.get(path=url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert board_response.data['title'] != title

    def test_delete_board_as_owner(self, auth_client, board_participant, board):
        """Test creator can delete the board."""

        url = reverse('detail_board', kwargs={'pk': board.pk})

        response = auth_client.delete(path=url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_board_as_writer(self, auth_client, create_board_for_test_writer):
        """Test writer can delete the board."""

        board = create_board_for_test_writer
        url = reverse('detail_board', kwargs={'pk': board.pk})

        response = auth_client.delete(path=url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_board_as_reader(self, auth_client, create_board_for_test_reader):
        """Test reader can delete the board."""

        board = create_board_for_test_reader
        url = reverse('detail_board', kwargs={'pk': board.pk})

        response = auth_client.delete(path=url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
