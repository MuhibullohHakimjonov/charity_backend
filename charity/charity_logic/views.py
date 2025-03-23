from rest_framework.permissions import IsAuthenticated

from .models import Needy, Reviews
from .serializers import NeedySerializer, ReviewsSerializer
from rest_framework.viewsets import ModelViewSet


class NeedyViewSet(ModelViewSet):
    queryset = Needy.objects.all()
    serializer_class = NeedySerializer


class ReviewsViewSet(ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
