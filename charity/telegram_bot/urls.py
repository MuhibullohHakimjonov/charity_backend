from django.urls import path
from .views import save_phone_number, get_questions, SaveResponsesView, check_user_status, get_audio

urlpatterns = [
    path("save_phone/", save_phone_number),
    path("questions/", get_questions),
    path("responses/", SaveResponsesView.as_view()),
    path("check_user/<int:user_id>/", check_user_status),
    path("get_audio/", get_audio),
]
