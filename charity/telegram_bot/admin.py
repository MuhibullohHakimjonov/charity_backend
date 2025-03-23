from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Question, UserPhone, UserResponse


@admin.register(Question)
class QuestionAdmin(ModelAdmin):
    list_display = ("id", "text")
    search_fields = ("text",)
    ordering = ("id",)


@admin.register(UserPhone)
class UserPhoneAdmin(ModelAdmin):
    list_display = ("user_id", "username", "phone_number")
    search_fields = ("username", "phone_number")
    ordering = ("user_id",)


@admin.register(UserResponse)
class UserResponseAdmin(ModelAdmin):
    list_display = ("user", "question", "response", "timestamp")
    list_filter = ("timestamp",)
    search_fields = ("user__username", "response")
    ordering = ("-timestamp",)
