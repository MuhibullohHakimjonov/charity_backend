from rest_framework import serializers
from .models import Needy, Reviews


class NeedySerializer(serializers.ModelSerializer):
    class Meta:
        model = Needy
        fields = ['id', 'title', 'description', 'created_at']


class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ['id', 'title', 'description', 'author', 'created_at']
