import os

from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver


class Question(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text


def validate_audio_file(value):
    valid_extensions = ['.mp3', '.ogg']
    if not any(value.name.lower().endswith(ext) for ext in valid_extensions):
        raise ValidationError("Only MP3 and MP4 files are allowed.")


class AdminAudio(models.Model):
    audio = models.FileField(upload_to="audios/", validators=[validate_audio_file])

    def __str__(self):
        return self.audio.name

    class Meta:
        verbose_name = 'Audio'
        verbose_name_plural = 'Audios'


class UserPhone(models.Model):
    user_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.username} ({self.phone_number})"

    class Meta:
        verbose_name = 'Telegram User'
        verbose_name_plural = 'Telegram Users'


class UserResponse(models.Model):
    user = models.ForeignKey(UserPhone, on_delete=models.CASCADE, related_name="responses")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} -> {self.question.text}: {self.response}"
