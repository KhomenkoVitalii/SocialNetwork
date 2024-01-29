from main.models import Like
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status


class LikeModelMixin():
    @action(methods=['post'], detail=True, url_name="like")
    def like_action(self, request, *args, **kwargs):
        obj = self.get_object()

        if obj.likes.filter(user=request.user).exists():
            return Response({"status": "You already liked this post!"}, status=status.HTTP_400_BAD_REQUEST)

        Like.objects.create(user=request.user, content_object=obj).save()
        return Response({"status": "liked"}, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True, url_name="unlike")
    def unlike_action(self, request, *args, **kwargs):
        obj = self.get_object()

        like = obj.likes.filter(user=request.user)
        if not like.exists():
            return Response({"status": "You haven't liked this post!"}, status=status.HTTP_400_BAD_REQUEST)

        like.delete()
        return Response({"status": "unliked!"}, status=status.HTTP_202_ACCEPTED)
