from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from django.contrib.auth import get_user_model
from .models import Post, Like
from .serializers import PostSerializer, AnalyticsSerializer
from .mixins import LikeModelMixin
from datetime import datetime

User = get_user_model()


class PostViewSet(ModelViewSet, LikeModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikesAnalytics(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        date_from_str = request.GET.get('date_from')
        date_to_str = request.GET.get('date_to')

        if not date_from_str or not date_to_str:
            return Response({'error': 'Both date_from and date_to parameters are required'}, status=400)

        try:
            date_from = datetime.strptime(date_from_str, '%Y-%m-%d').date()
            date_to = datetime.strptime(date_to_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid date format. Please use YYYY-MM-DD'}, status=400)

        likes_analytics = Like.objects.filter(created_at__range=(date_from, date_to)) \
            .values('created_at') \
            .annotate(total_likes=Count('id'))

        analytics_data = [
            {'date': item['created_at__date'],
                'total_likes': item['total_likes']}
            for item in likes_analytics
        ]

        return Response(analytics_data)


class UserActivity(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, username):
        user = User.objects.get(username=username)
        last_login = user.last_login.strftime(
            '%Y-%m-%d %H:%M:%S') if user.last_login else None
        last_request = user.last_request.strftime(
            '%Y-%m-%d %H:%M:%S') if hasattr(user, 'last_request') else None

        activity_data = {
            'username': username,
            'last_login': last_login,
            'last_request': last_request
        }

        return Response(activity_data)
