from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Quiz, Answer, Question
from .forms import CandidateForm
from .services import save_result, filter_quiz, create_quiz_from_docx


@csrf_exempt
def upload_quiz_view(request):
    """View для отправки теста"""
    if request.method == 'POST':
        file = request.FILES.get('docx_file')

        if file:
            result = create_quiz_from_docx(file)
            return JsonResponse({'result': result})

    return JsonResponse({'error': 'Invalid request'})


def get_quiz_list(request):
    """View для получения списка всех тестов"""
    quiz = Quiz.objects.all()
    quiz_list = list(quiz.values())
    return JsonResponse({'quiz': quiz_list})

@csrf_exempt
def get_info_and_quiz(request, quiz):
    """View которое сначало просит пользователя заполнить форму с информацияей о себе, а затем отправляет ему выбранный тест"""
    if request.method == 'POST':
        form = CandidateForm(request.POST)
        if form.is_valid():
            candidate = form.save()
            request.session['candidate_id'] = candidate.id  # Сохраняем только ID кандидата в сессии
            q, ans = filter_quiz(quiz)

            return JsonResponse({
                'candidate_id': candidate.id,  # Передаем только ID кандидата, а не сам объект
                'candidate_fullname': candidate.fullname,  # Пример передачи других данных о кандидате
                'quiz': quiz,
                'questions': list(q),
                'answers': list(ans)
            })
    else:
        form = CandidateForm()

    return JsonResponse({'form': form.as_p()})

@csrf_exempt
def get_result(request, quiz):
    """View которое предназначенно для сохранения результата прохождения тестирования"""
    if request.method == 'POST':
        candidate = request.session.get('candidate_id')
        questions = Question.objects.filter(quiz=quiz)
        save_result(candidate, quiz, request.POST, len(questions))
        return JsonResponse({'success': 'Result submitted'})
    return JsonResponse({'error': 'Invalid request'})


