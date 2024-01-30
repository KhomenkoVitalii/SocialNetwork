from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.contenttypes import fields, models as contrib_models
from .utils import normalize_phone_number


class AppUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, phone_number, email, password=None, **kwargs):
        if not first_name:
            raise ValueError('A first name is required!')
        if not last_name:
            raise ValueError('A last name is required!')
        if not email:
            raise ValueError('An email is required!')
        if not phone_number:
            raise ValueError('An phone number is required!')
        if not username:
            raise ValueError('An username is required!')
        if not password:
            raise ValueError('An password is required!')

        email = self.normalize_email(email)
        norm_phone_number = normalize_phone_number(phone_number)

        user = self.model(email=email,
                          first_name=first_name,
                          last_name=last_name,
                          username=username,
                          phone_number=norm_phone_number)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, first_name, last_name, username, phone_number, email, password=None, **kwargs):
        if not first_name:
            raise ValueError('A first name is required!')
        if not last_name:
            raise ValueError('A last name is required!')
        if not email:
            raise ValueError('An email is required!')
        if not phone_number:
            raise ValueError('An phone number is required!')
        if not username:
            raise ValueError('An username is required!')
        if not password:
            raise ValueError('An password is required!')

        user = self.create_user(first_name, last_name, username,
                                phone_number, email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class AppUser(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=254, unique=True, null=False)
    phone_number = models.CharField(null=False, unique=True)

    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)

    username = models.CharField(max_length=100, null=False, unique=True)

    image = models.ImageField(upload_to="uploads/images/users/", null=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateField(
        auto_now_add=True, null=False, editable=False)

    groups = models.ManyToManyField(
        'auth.Group', related_name='app_users', blank=True)
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='app_users', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',
                       'phone_number', 'username']

    class Meta:
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['username']),
            models.Index(fields=['created_at']),
        ]

    objects = AppUserManager()

    def __str__(self):
        return self.username


class Like(models.Model):
    user = models.ForeignKey(
        AppUser, on_delete=models.CASCADE, related_name='main_user')

    # Abstraction, because we can use likes not only on the post (for example it can be also comments)
    content_type = models.ForeignKey(
        contrib_models.ContentType, on_delete=models.CASCADE, related_name='liked_obj')
    object_id = models.PositiveIntegerField()
    content_object = fields.GenericForeignKey()

    created_at = models.DateField(
        auto_now_add=True, null=False, editable=False)

    class Meta:
        indexes: [
            models.Index(fields=['user'])
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'content_type', 'object_id'], name='unique_like')
        ]

    def __str__(self):
        return f"Like by {self.user.username} on {self.content_object}"


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=255)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    img = models.ImageField(
        upload_to='uploads/images/%Y/%m/%d/', blank=True, null=True)
    is_safe = models.BooleanField(default=True)
    likes = fields.GenericRelation('Like')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateField(
        auto_now_add=True, null=False, editable=False)

    class Meta:
        indexes: [
            models.Index(fields=['user']),
            models.Index(fields=['created_at']),
            models.Index(fields=['title'])
        ]

    def __str__(self):
        return self.title
