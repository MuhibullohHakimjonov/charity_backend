from django.db import models


class TelegramUser(models.Model):
    user_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.user_id})"


class Reviews(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=255)

    def __str__(self):
        return f'Review title: {self.title}. Created at: {self.created_at}'


class Needy(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Title: {self.title}. Created at: {self.created_at}'


class ReviewsImage(models.Model):
    reviews = models.ForeignKey(Reviews, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='images/', blank=True, null=True)


class NeedyImage(models.Model):
    needy = models.ForeignKey(Needy, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='images/', blank=True, null=True)
