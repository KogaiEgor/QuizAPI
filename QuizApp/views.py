from django.shortcuts import render
from django.http import JsonResponse
from .quizparse import create_quiz_from_docx
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def upload_quiz_view(request):
    if request.method == 'POST':
        file = request.FILES.get('docx_file')

        if file:
            # Передаем .docx файл в функцию create_quiz_from_docx
            result = create_quiz_from_docx(file)

            # Возвращаем результат обработки в виде JSON
            return JsonResponse({'result': result})

    return JsonResponse({'error': 'Invalid request'})

