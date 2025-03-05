from django.urls import path, include
from .views import register_telegram_user, NeedyViewSet, ReviewsViewSet, redirect_to_bot
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('needy', NeedyViewSet)
router.register('reviews', ReviewsViewSet)

urlpatterns = [
    path('register-user/', register_telegram_user, name='register-user'),
    path('redirect-to-bot/', redirect_to_bot, name='redirect-to-bot'),
    path('', include(router.urls))
]
