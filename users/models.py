from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers

        
class UserManger(BaseUserManager):
    def create_user(self, username, email, password=None):
        password = serializers.CharField(max_length=68, min_length=6, write_only=True)
        if username is None:
            raise TypeError('User should have username')
        if email is None:
            raise TypeError('User should have email')

        user = self.model(username=username,email=self.normalize_email(email))

        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user



class User(AbstractBaseUser, PermissionsMixin):
    
    COHORTS = {
        ('py-d6', 'py-d6'),
    }
    ROLES = {
        ('student', 'Student'),
        ('ta', 'TA'),
        ('instructor', 'Instructor'),
    }
    cohort = models.CharField(max_length=80, choices=COHORTS, blank=True, default='py-d6')
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    role = models.CharField(max_length=80, choices=ROLES, default='student')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    fulfilled_points = models.IntegerField(blank=True, default=0)
    total_points = models.IntegerField(blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManger()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


class RandomUser(models.Model):
    username = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)