from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model



class UserProfile(AbstractUser):
    pin = models.CharField(max_length=10, unique=True, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='user_profiles',
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='user_profiles',
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
        related_query_name='user_profile',
    )

    def __str__(self):
        return self.username


class Conversation(models.Model):
    user1 = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='conversations1')
    user2 = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='conversations2')
    last_message_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation between {self.user1.username} and {self.user2.username}"

    def get_other_user(self, user):
        if user == self.user1:
            return self.user2
        elif user == self.user2:
            return self.user1


class Message(models.Model):
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='received_messages')
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)


