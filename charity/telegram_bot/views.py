from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from .models import UserPhone, Question, UserResponse, AdminAudio
from .serializers import UserPhoneSerializer, QuestionSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def save_phone_number(request):
    serializer = UserPhoneSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Phone number saved"}, status=201)
    return Response(serializer.errors, status=400)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_questions(request):
    questions = Question.objects.all()
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)


class SaveResponsesView(APIView):
    def post(self, request):
        responses = request.data.get("responses", [])
        if not responses:
            return Response({"error": "No responses provided"}, status=400)

        for response in responses:
            user, _ = UserPhone.objects.get_or_create(user_id=response["user_id"])
            UserResponse.objects.create(
                user=user,
                question_id=response["question"],
                response=response["response"]
            )

        return Response({"message": "Responses saved successfully"}, status=201)


@api_view(["GET"])
@permission_classes([AllowAny])
def check_user_status(request, user_id):
    user_exists = UserPhone.objects.filter(user_id=user_id).exists()
    quiz_completed = UserResponse.objects.filter(user__user_id=user_id).exists()

    if user_exists and quiz_completed:
        return Response({"status": "completed"}, status=200)
    elif user_exists:
        return Response({"status": "registered"}, status=200)
    return Response({"status": "not_registered"}, status=404)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_audio(request):
    audio = AdminAudio.objects.first()
    if audio:
        return Response({"audio_url": audio.audio.url})
    return Response({"audio_url": None})
