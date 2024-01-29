from pytest import fixture
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from main.models import Post

User = get_user_model()

user_test_data = {
    'email': 'user@gmail.com',
    'phone_number': '+380567341385',
    'username': 'user',
    'first_name': 'User',
    'last_name': 'User',
    'password': '12345678'
}

post_test_data = {
    'title': 'Test title',
    'body': 'Test body',
}


@fixture
def api_client():
    return APIClient()


@fixture
def user(db):
    return User.objects.create_user(**user_test_data)


@fixture
def authorized_user(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@fixture
def post(api_client, user, authorized_user):
    return Post.objects.create(user=authorized_user, **post_test_data)
