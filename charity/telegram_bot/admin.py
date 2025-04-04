from django.contrib import admin
from django import forms
from unfold.admin import ModelAdmin
from .models import Question, UserPhone, UserResponse, AdminAudio, validate_audio_file


@admin.register(Question)
class QuestionAdmin(ModelAdmin):
    list_display = ("id", "text")
    search_fields = ("text",)
    ordering = ("id",)


class AdminAudioForm(forms.ModelForm):
    class Meta:
        model = AdminAudio
        fields = "__all__"

    def clean_audio(self):
        audio = self.cleaned_data.get("audio")
        if audio:
            validate_audio_file(audio)
        return audio


@admin.register(AdminAudio)
class AdminAudioAdmin(admin.ModelAdmin):
    form = AdminAudioForm
    list_display = ['id', "audio"]
    list_display_links = ['id', 'audio']


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
    ordering = ("timestamp",)
