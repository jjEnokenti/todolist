import uuid

import pytest
from rest_framework import status
from rest_framework.reverse import reverse


@pytest.mark.django_db
class TestUserAPI:
    """User API tests."""

    def test_create_new_user(self, client):
        """Test create new user and check response data."""

        url = reverse('user_register')

        payload = {
            'username': 'test_user',
            'password': '12345ewqqwe',
            'password_repeat': '12345ewqqwe',
            'first_name': 'TEST',
            'email': 'test@example.com'
        }

        response = client.post(path=url, data=payload)

        expected_data = {
            'id': response.data['id'],
            'username': 'test_user',
            'first_name': 'TEST',
            'last_name': '',
            'email': 'test@example.com',
            'role': 'user'
        }
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == expected_data
        assert response.data.get('password') is None

    def test_create_new_user_with_exist_username(self, client, user):
        """Test create new user with already exist username in db."""

        url = reverse('user_register')

        payload = {
            'username': user.username,
            'password': '12345ewqqwe',
            'password_repeat': '12345ewqqwe',
            'email': 'test@example.com'
        }

        response = client.post(path=url, data=payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['username'] == ['A user with that username already exists.']

    def test_create_new_user_with_incorrect_repeat_password(self, client):
        """Test create new user with incorrect repeat password."""

        url = reverse('user_register')

        payload = {
            'username': 'test_user',
            'password': '12345ewqqwe',
            'password_repeat': 'weqeqeqeqeewewq123123123',
            'first_name': 'TEST',
            'email': 'test@example.com'
        }

        response = client.post(path=url, data=payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['password'] == ['the password and the repeat password must match.']

    def test_create_new_user_with_invalid_password(self, client):
        """Test create new user with invalid password."""

        url = reverse('user_register')

        payload = {
            'username': 'test_user',
            'password': '12345e',
            'password_repeat': '12345e',
            'first_name': 'TEST',
            'email': 'test@example.com'
        }

        response = client.post(path=url, data=payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_new_user_with_invalid_email(self, client):
        """Test create new user with incorrect repeat password."""

        url = reverse('user_register')

        payload = {
            'username': 'test_user',
            'password': '12345ewqqwe',
            'password_repeat': '12345ewqqwe',
            'first_name': 'TEST',
            'email': 'testexample.com'
        }

        response = client.post(path=url, data=payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['email'] == ['Enter a valid email address.']

    def test_user_login_valid_credentials(self, auth_client, user, password):
        url = reverse('user_login')

        payload = {
            'username': user.username,
            'password': password
        }

        response = auth_client.post(path=url, data=payload, content_type='application/json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == user.username

    def test_user_login_invalid_credentials(self, auth_client, user):
        url = reverse('user_login')

        payload = {
            'username': user.username,
            'password': '123'
        }

        response = auth_client.post(path=url, data=payload, content_type='application/json')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_user_login_blank_password_field(self, auth_client, user):
        url = reverse('user_login')

        payload = {
            'username': user.username,
            'password': ''
        }

        response = auth_client.post(path=url, data=payload, content_type='application/json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['password'] == ['This field may not be blank.']

    def test_user_update_password_ok(self, password, auth_client):
        url = reverse('update_password')

        payload = {
            'old_password': password,
            'new_password': uuid.uuid4()
        }

        response = auth_client.put(path=url, data=payload, content_type='application/json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {}

    def test_user_update_password_incorrect_old_password(self, auth_client, password):
        url = reverse('update_password')

        payload = {
            'old_password': 'incorrect_password',
            'new_password': uuid.uuid4()
        }

        response = auth_client.put(path=url, data=payload, content_type='application/json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['current password'] == 'incorrect current password.'

    def test_user_update_password_invalid_new_password(self, password, auth_client):
        url = reverse('update_password')

        payload = {
            'old_password': password,
            'new_password': 'password'
        }

        response = auth_client.put(path=url, data=payload, content_type='application/json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['password'] == ['This password is too common.']

    def test_user_update_profile(self, auth_client):
        url = reverse('user_profile')

        payload = {
            'username': 'NEW_TEST_USERNAME',
        }

        response = auth_client.put(path=url, data=payload, content_type='application/json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == 'NEW_TEST_USERNAME'

    def test_user_update_profile_with_invalid_data(self, auth_client):
        url = reverse('user_profile')

        payload = {
            'email': '1'
        }

        response = auth_client.put(path=url, data=payload, content_type='application/json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['email'] == ['Enter a valid email address.']

    def test_user_update_profile_username_exist(self, auth_client, user_factory):
        url = reverse('user_profile')

        user_factory.create(username='username')

        payload = {
            'username': 'username',
        }

        response = auth_client.put(path=url, data=payload, content_type='application/json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['username'] == ['A user with that username already exists.']

    def test_user_logout_ok(self, auth_client):
        url = reverse('user_profile')

        response = auth_client.delete(path=url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_not_login_user_try_logout(self, client):
        url = reverse('user_profile')

        response = client.delete(path=url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data['detail'] == 'Authentication credentials were not provided.'
