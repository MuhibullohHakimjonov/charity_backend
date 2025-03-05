from django.shortcuts import redirect
from .models import Needy, Reviews, TelegramUser
from .serializers import NeedySerializer, ReviewsSerializer
from rest_framework.viewsets import ModelViewSet
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests

TELEGRAM_BOT_TOKEN = "7003776520:AAHlIQly8I9E7_Ss90Up4McNpJSwwuAAgpY"
ADMIN_CHAT_ID = "1380803567"

BOT_USERNAME = "r_e_d_H_e_A_Dbot"


def redirect_to_bot(request):
    """Redirect user to Telegram bot"""
    return redirect(f"https://t.me/{BOT_USERNAME}")


def notify_admin(user_id, username):
    """Notify admin when a new user joins"""
    message = f"🚀 New User Started Bot!\n🆔 User ID: {user_id}\n👤 Username: @{username}"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": ADMIN_CHAT_ID, "text": message}
    requests.post(url, json=payload)


@csrf_exempt
def register_telegram_user(request):
    """Save new Telegram users when they press /start"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("Received Data:", data)  # Debugging

            user_id = data.get("user_id")
            username = data.get("username") or "No Username"

            user, created = TelegramUser.objects.get_or_create(
                user_id=user_id,
                defaults={"username": username}
            )

            if created:
                notify_admin(user_id, username)

            return JsonResponse({"status": "success", "message": f"User {username} registered."})

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON format"}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


class NeedyViewSet(ModelViewSet):
    queryset = Needy.objects.all()
    serializer_class = NeedySerializer


class ReviewsViewSet(ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
