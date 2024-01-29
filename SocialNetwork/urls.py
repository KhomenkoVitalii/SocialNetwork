"""
URL configuration for SocialNetwork project.
"""

from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from main.views import PostViewSet, LikesAnalytics, UserActivity
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

router = routers.DefaultRouter()

router.register(r'api/posts', PostViewSet, basename='post')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include('djoser.urls.jwt')),
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/v1/docs/',
         SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-docs'),
    path('api/analytics/', LikesAnalytics.as_view(), name='likes-analytics'),
    path('api/user-activity/<str:username>/',
         UserActivity.as_view(), name='user-activity'),
]

urlpatterns += router.urls
