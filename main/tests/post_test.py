import pytest
from main.models import Post
from main.serializers import PostSerializer
from django.urls import reverse
from django.contrib.auth import get_user_model
from main.tests.fixtures import post_test_data, api_client, user, authorized_user, post
from rest_framework import status

User = get_user_model()


@pytest.mark.django_db
class TestPostApi:
    def test_get_posts(self, api_client, authorized_user, post):
        response = authorized_user.get(reverse('post-list'))

        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

        serialized_data = PostSerializer(post).data

        assert response.data and serialized_data, "Response data is empty or does not match serialized data"

    def test_create_post(self, api_client, user, authorized_user, post):
        response = authorized_user.post(reverse('post-list'), {
            'title': post_test_data.get('title'),
            'body': post_test_data.get('body'),
            'user': user.id}, format='json')

        assert response.status_code == 201

        assert response.data['title'] == post.title
        assert response.data['body'] == post.body
        assert response.data['user'] == user.id

    def test_retrieve_post(self, api_client, authorized_user, post):
        url = reverse('post-detail', args=[post.id])

        response = authorized_user.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == post.title
        assert response.data['body'] == post.body
        assert response.data['user'] == post.user.id

    def test_retrieve_nonexistent_post(self, api_client, authorized_user):
        # Assuming post with ID 999 doesn't exist
        url = reverse('post-detail', args=[999])

        response = authorized_user.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_post(self, api_client, authorized_user, post):
        updated_title = 'Updated Title'
        updated_body = 'Updated Body'

        url = reverse('post-detail', args=[post.id])
        updated_data = {'title': updated_title,
                        'body': updated_body, 'user': post.user.id}

        response = authorized_user.put(url, updated_data, format='json')
        assert response.status_code == status.HTTP_200_OK

        # Refresh the post
        post.refresh_from_db()
        assert post.title == updated_title
        assert post.body == updated_body

    def test_delete_post(self, api_client, authorized_user, post):
        url = reverse('post-detail', args=[post.id])

        response = authorized_user.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify that the post has been deleted from the database
        with pytest.raises(Post.DoesNotExist):
            Post.objects.get(id=post.id)
