from django.contrib import admin
from .models import Needy, NeedyImage, ReviewsImage, Reviews, TelegramUser
from unfold.admin import ModelAdmin


class ReviewsImageInline(admin.TabularInline):
    model = ReviewsImage
    fk_name = 'reviews'
    extra = 3


class NeedyImageInline(admin.TabularInline):
    model = NeedyImage
    fk_name = 'needy'
    extra = 3


@admin.register(Needy)
class NeedyAdmin(ModelAdmin):
    inlines = [NeedyImageInline]
    list_display = ['id', 'title', 'description', 'created_at']
    list_display_links = ['id', 'title']


@admin.register(Reviews)
class ReviewsAdmin(ModelAdmin):
    inlines = [ReviewsImageInline]
    list_display = ['id', 'title', 'description', 'author', 'created_at']
    list_display_links = ['id', 'title']


@admin.register(TelegramUser)
class ReviewsAdmin(ModelAdmin):
    list_display = ['id', 'user_id', 'username', 'joined_at']
    list_display_links = ['id', 'user_id']
