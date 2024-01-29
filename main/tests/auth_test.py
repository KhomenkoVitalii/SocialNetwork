import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED


@pytest.mark.django_db
def test_user_creation(api_client, user_test_data):
    url = reverse('auth_users_create')
    response = api_client.post(url, user_test_data, format='json')
    assert response.status_code == HTTP_201_CREATED


@pytest.mark.django_db
def test_user_gets_jwt_tokens(api_client, user_test_data):
    url = reverse('jwt-create')
    response = api_client.post(url, {'email': user_test_data.get(
        'email'), 'password': user_test_data.get('password')}, format='json')
    assert response.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_user_logout(api_client, authorized_user):
    url = reverse('logout')
    response = api_client.post(url, format='json')
    assert response.status_code == HTTP_200_OK
