"""
URL configuration for QuizAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from QuizApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('uploadquiz/', views.upload_quiz_view),
    path('quizlist/', views.get_quiz_list),
    path('getquiz/<int:quiz>/', views.get_info_and_quiz),
    path('getquiz/<int:quiz>/getresult/', views.get_result),
]
