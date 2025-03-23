from django.urls import path, include
from .views import NeedyViewSet, ReviewsViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('needy', NeedyViewSet)
router.register('reviews', ReviewsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
