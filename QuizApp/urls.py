from django.urls import path
from .views import *


urlpatterns = [
    path('uploadquiz/', UploadQuizView.as_view()),
    path('quizlist/', GetQuizList.as_view()),
    path('getquiz/<int:quiz>/', GetInfoAndQuiz.as_view()),
    path('getquiz/<int:quiz>/getresult/', SaveResultView.as_view()),
]