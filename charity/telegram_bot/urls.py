from django.urls import path

from .views import redirect_to_bot, QuestionListView, SavePhoneNumberView, SaveUserResponseView

urlpatterns = [
    path('redirect-to-bot/', redirect_to_bot, name='redirect-to-bot'),
    path("questions/", QuestionListView.as_view(), name="question-list"),
    path("save_phone/", SavePhoneNumberView.as_view(), name="save_phone"),
    path("responses/", SaveUserResponseView.as_view(), name="user-response-create"),
]
