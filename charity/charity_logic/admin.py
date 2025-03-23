from django.contrib import admin
from .models import Needy, NeedyImage, ReviewsImage, Reviews, CharityStatistics
from unfold.admin import ModelAdmin
from user_auth.models import CustomUser


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


@admin.register(CustomUser)
class CustomUserAdmin(ModelAdmin):
    list_display = ['id', 'email', 'username']
    list_display_links = ['id', 'email']


@admin.register(CharityStatistics)
class CharityStatisticsAdmin(ModelAdmin):
    list_display = ['id', 'total_donations']
    list_display_links = ['id', 'total_donations']
