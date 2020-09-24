from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    A custom User class that inherits Django's default User model
    to be able to easily extend it's functionality
    if the need arises in the future.
    """
    pass


class Post(models.Model):
    """
    The model used to store all posts from the Wall app.
    """
    time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
