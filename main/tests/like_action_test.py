import pytest
from django.urls import reverse
from rest_framework import status
from main.models import Post, Like
from rest_framework.test import APIClient
from main.tests.fixtures import api_client, user_test_data, post
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_like_post(api_client, authorized_user, post):
    url = reverse('post-like', kwargs={'pk': post.id})
    response = authorized_user.post(url)
    assert response.status_code == status.HTTP_201_CREATED
    assert post.likes.count() == 1


@pytest.mark.django_db
def test_unlike_post(api_client, authorized_user, post):
    like = Like.objects.create(user=authorized_user, content_object=post)
    url = reverse('post-unlike', kwargs={'pk': post.id})
    response = authorized_user.post(url)
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert post.likes.count() == 0


@pytest.mark.django_db
def test_like_already_liked_post(api_client, authorized_user, post):
    Like.objects.create(user=authorized_user, content_object=post)
    url = reverse('post-like', kwargs={'pk': post.id})
    response = authorized_user.post(url)
    url = reverse('post-like', kwargs={'pk': post.id})
    response = authorized_user.post(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_unlike_unliked_post(api_client, authorized_user, post):
    url = reverse('post-unlike', kwargs={'pk': post.id})
    response = authorized_user.post(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
