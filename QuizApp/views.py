from .services import save_result, filter_quiz, create_quiz_from_docx, CreatorPermission, check_creator
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from .serializers import *
from rest_framework.permissions import AllowAny
from django.shortcuts import redirect


class SeeResults(ListAPIView):
    serializer_class = ResultSerializer
    permission_classes = [CreatorPermission]
    def get_queryset(self):
        quiz_id = self.kwargs.get('quiz')
        return Result.objects.filter(quiz_id=quiz_id)

class CreateCreator(CreateAPIView):
    serializer_class = CreatorSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            creator = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UploadQuizView(APIView):
    permission_classes = [CreatorPermission]
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)

        if serializer.is_valid():
            file = serializer.validated_data['docx_file']
            result = create_quiz_from_docx(file, self.kwargs['creator_id'])
            return Response({'result': result}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetQuizList(ListAPIView):
    serializer_class = QuizSerializer

    def get_queryset(self):
        creator_id = self.kwargs.get('creator_id')
        return Quiz.objects.filter(creator__id=creator_id)

    def post(self, request, creator_id):
        telegram_id = request.data.get('telegram_id')
        quiz_id = request.data.get('quiz_id')
        is_creator = check_creator(telegram_id)

        if is_creator:
            return redirect(f'/{creator_id}/seeresults/{quiz_id}/')
        else:
            return redirect(f'/{creator_id}/getquiz/{quiz_id}/')

class GetInfoAndQuiz(APIView):
    def post(self, request, quiz, creator_id):
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
    def post(self, request, quiz, creator_id):
        result = save_result(candidate_id=request.session.get('candidate_id'), quiz_id=quiz,
                             result=request.data, question_count=request.session.get('number_of_questions'))
        if isinstance(result, Result):
            return Response({'success': 'Result submitted'}, status=status.HTTP_200_OK)
        return Response({'error': result}, status=status.HTTP_400_BAD_REQUEST)
