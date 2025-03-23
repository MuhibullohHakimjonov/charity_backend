from django.db import models
from django.conf import settings

class Reviews(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Reviews"

    def __str__(self):
        return f'Review title: {self.title}. Created at: {self.created_at}'


class Needy(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "People Who Need Help"
        verbose_name_plural = "People Who Need Help"

    def __str__(self):
        return f'Title: {self.title}. Created at: {self.created_at}'


class ReviewsImage(models.Model):
    reviews = models.ForeignKey(Reviews, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='images/', blank=True, null=True)


class NeedyImage(models.Model):
    needy = models.ForeignKey(Needy, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='images/', blank=True, null=True)


class CharityStatistics(models.Model):
    total_donations = models.DecimalField(max_digits=15, decimal_places=2, help_text="Total amount donated")
    total_human_who_donations = models.PositiveIntegerField(default=0, help_text='How many people have donated')

    def __str__(self):
        return f"Statistics as of {self.last_updated.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name = "Charity Statistics"
        verbose_name_plural = "Charity Statistics"
