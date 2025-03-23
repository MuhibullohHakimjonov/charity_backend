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

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['author'] = request.user
        return super().create(validated_data)
