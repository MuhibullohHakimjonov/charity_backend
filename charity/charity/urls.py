from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static, settings

from payment.views import PaymeCallBackAPIView

from payment.views import ClickWebhookAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('charity_logic.urls')),
    path('telegram/', include('telegram_bot.urls')),
    path("auth/", include("user_auth.urls")),
    path('payment/', include('payment.urls')),
    path("payment/update/", PaymeCallBackAPIView.as_view()),
    path("payment/click/update/", ClickWebhookAPIView.as_view()),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
