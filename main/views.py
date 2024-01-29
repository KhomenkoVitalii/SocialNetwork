from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from .models import Post
from .serializers import PostSerializer
from .mixins import LikeModelMixin

User = get_user_model()


class PostViewSet(ModelViewSet, LikeModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
