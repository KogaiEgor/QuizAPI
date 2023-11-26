from django.urls import path
from .views import *


urlpatterns = [
    path('creator/', CreateCreator.as_view()),
    path('/<int:creator_id>/seeresults/<int:quiz>/', SeeResults.as_view()),
    path('<int:creator_id>/uploadquiz/', UploadQuizView.as_view()),
    path('<int:creator_id>/quizlist/', GetQuizList.as_view()),
    path('<int:creator_id>/getquiz/<int:quiz>/', GetInfoAndQuiz.as_view()),
    path('<int:creator_id>/getquiz/<int:quiz>/getresult/', SaveResultView.as_view()),
]



