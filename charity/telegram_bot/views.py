import os
from django.shortcuts import redirect
import requests
from dotenv import load_dotenv
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Question, UserResponse, UserPhone
from .serializers import QuestionSerializer
from user_auth.models import CustomUser

load_dotenv()

BOT_USERNAME = os.getenv("BOT_USERNAME")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")


def redirect_to_bot(request):
    return redirect(f"https://t.me/{BOT_USERNAME}")


def notify_admin(user_id, username):
    message = f"🚀 New User Started Bot!\n🆔 User ID: {user_id}\n👤 Username: @{username}"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": ADMIN_CHAT_ID, "text": message}
    requests.post(url, json=payload)


class QuestionListView(ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class SavePhoneNumberView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_id = request.data.get("user_id")
        username = request.data.get("username")
        phone_number = request.data.get("phone_number")

        if not user_id or not phone_number:
            return Response({"error": "User ID and phone number are required"}, status=400)

        user, created = UserPhone.objects.update_or_create(
            user_id=user_id,
            defaults={"username": username, "phone_number": phone_number}
        )
        return Response({"message": "Phone number saved successfully"})


class SaveUserResponseView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_id = request.data.get("user_id")
        username = request.data.get("username")
        question_id = request.data.get("question")
        response_text = request.data.get("response")

        try:
            user = UserPhone.objects.get(user_id=user_id)
        except UserPhone.DoesNotExist:
            return Response({"error": "User not found. Please register your phone number first."}, status=400)

        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return Response({"error": "Question not found"}, status=400)

        UserResponse.objects.create(user=user, question=question, response=response_text)

        return Response({"message": "Response saved successfully"})
