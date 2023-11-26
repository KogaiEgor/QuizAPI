from rest_framework import serializers
from .models import *


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'

class FileUploadSerializer(serializers.Serializer):
    docx_file = serializers.FileField()

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class ResultSerializer(serializers.ModelSerializer):
    result = serializers.CharField(read_only=True)
    class Meta:
        model = Result
        fields = ['candidate', 'quiz', 'result']
        read_only_fields = ['result']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'

    def validate_email(self, value):
        if Candidate.objects.filter(email=value).exists():
            raise serializers.ValidationError("Этот email уже занят")
        return value

class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creator
        fields = '__all__'

    def validate(self, attrs):
        telegram_id = attrs.get('telegram_id')
        if telegram_id is not None and Creator.objects.filter(telegram_id=telegram_id).exists():
            raise serializers.ValidationError("Этот telegram уже зарегистрирован")
        return attrs

