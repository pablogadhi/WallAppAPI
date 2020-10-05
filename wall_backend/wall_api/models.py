from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail


class User(AbstractUser):
    """
    A custom User class that inherits Django's default User model
    to be able to easily extend it's functionality
    if the need arises in the future.
    """
    pass


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    Creates a token automaticaly for a recently created user
    and sends and email to his email address.
    """
    if created:
        Token.objects.create(user=instance)
        send_mail('Thank\'s for joining Wall App', 'We are really glad to have you here!',
                  'staff@wallapp.com', [instance.email], fail_silently=True)


class Post(models.Model):
    """
    The model used to store all posts from the Wall app.
    """
    time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['time']
