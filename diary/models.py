from django.db import models
from django.contrib.auth.models import User

class Entry(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    EMOTION_CHOICES = [
        ('happy', '행복'),
        ('sad', '슬픔'),
        ('angry', '분노'),
        ('joy', '즐거움'),
        ('lethargy', '무기력'),
    ]
    emotion = models.CharField(max_length=10, choices=EMOTION_CHOICES, default='neutral')

    def __str__(self):
        return self.title
