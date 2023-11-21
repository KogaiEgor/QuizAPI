from .services import save_result, filter_quiz, create_quiz_from_docx
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from .serializers import *


class UploadQuizView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)

        if serializer.is_valid():
            file = serializer.validated_data['docx_file']
            result = create_quiz_from_docx(file)
            return Response({'result': result}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetQuizList(ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class GetInfoAndQuiz(APIView):
    def post(self, request, quiz):
        serializer = CandidateSerializer(data=request.data)
        if serializer.is_valid():
            candidate = serializer.save()
            request.session['candidate_id'] = candidate.id

            q, ans, number_of_questions = filter_quiz(quiz)
            request.session['number_of_questions'] = number_of_questions
            return Response({
                'candidate_id': candidate.id,
                'candidate_fullname': candidate.fullname,
                'quiz': q,
                'answers': ans
            })

        return Response({'Error': serializer.errors})


class SaveResultView(APIView):
    def post(self, request, quiz):
        result = save_result(candidate_id=request.session.get('candidate_id'), quiz_id=quiz,
                             result=request.data, question_count=request.session.get('number_of_questions'))
        if isinstance(result, Result):
            return Response({'success': 'Result submitted'}, status=status.HTTP_200_OK)
        return Response({'error': result}, status=status.HTTP_400_BAD_REQUEST)
