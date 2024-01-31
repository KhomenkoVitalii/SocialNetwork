from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import Post, AppUser, Like
from .utils import normalize_phone_number


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'user', 'img',
                  'is_safe', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['email', 'password', 'phone_number', 'first_name',
                  'last_name', 'username', 'image', 'is_staff']

    def create(self, validated_data):
        user = AppUser.objects.create_user(**validated_data)
        return user


class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['id', 'email', 'phone_number', 'first_name',
                  'last_name', 'username', 'image', 'is_staff', 'created_at']
        read_only_fields = ['created_at']

    def validate_phone_number(self, value):
        try:
            normalized_phone_number = normalize_phone_number(value)
            return normalized_phone_number
        except ValueError as e:
            raise serializers.ValidationError(str(e))


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'content_type', 'object_id', 'created_at']
        read_only_fields = ['created_at']
