from rest_framework import serializers
from .models import Question, UserResponse, UserPhone, AdminAudio


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


class UserPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPhone
        fields = "__all__"


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserResponse
        fields = "__all__"


class AdminAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminAudio
        fields = "__all__"
