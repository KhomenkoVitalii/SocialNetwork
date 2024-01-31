import pytest
from django.urls import reverse
from main.tests.fixtures import api_client, get_user_test_data, user, authorized_user
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED


@pytest.mark.django_db
def test_user_creation(api_client, get_user_test_data):
    url = '/api/v1/auth/users/'
    response = api_client.post(url, get_user_test_data, format='json')
    assert response.status_code == HTTP_201_CREATED, response.content


@pytest.mark.django_db
def test_user_gets_jwt_tokens(api_client, get_user_test_data):
    url = '/api/v1/auth/users/'
    response = api_client.post(url, get_user_test_data, format='json')
    assert response.status_code == HTTP_201_CREATED, response.content

    url = reverse('jwt-create')
    response = api_client.post(
        url, {'email': get_user_test_data.get('email'), 'password': get_user_test_data.get('password')}, format='json')
    assert response.status_code == HTTP_200_OK, response.content
