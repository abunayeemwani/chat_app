from email.policy import default
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Member(AbstractUser):
    email = models.EmailField(
        verbose_name = 'Email Address',
        max_length = 255,
        unique = True
    )
    image = models.ImageField(upload_to='profile', default='profile/profile.png')

class ThreadManager(models.Manager):
    def by_user(self, **kwargs):
        user = kwargs.get('user')
        query = self.get_queryset().filter(
            models.Q(first_user=user) |
            models.Q(second_user=user)
        ).distinct()
        
        return query

class Thread(models.Model):
    first_user = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_first_person')
    second_user = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_second_person')
    date = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()
    class Meta:
        unique_together = ['first_user', 'second_user']

class Message(models.Model):
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.CASCADE, related_name='message_thread')
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)