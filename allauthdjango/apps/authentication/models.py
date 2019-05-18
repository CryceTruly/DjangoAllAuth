from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)

import jwt


class UserManager(BaseUserManager):
    def create_user(self, username, email, password):

        if username is None:
            raise TypeError('Username is required')
        if email is None:
            return TypeError('Email is required')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(unique=True)
    isActive = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    joined = models.DateTimeField(auto_now_add=True)
    updatedAow = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username

    def token(self):
        return createToken()

    def createToken(self):
        token = jwt.encode(
            {'username': self.username, 'email': self.email}, 'secret', algorithm='HS256')
        return token
