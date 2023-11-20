from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Quiz(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.content

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.content


class Candidate(models.Model):
    fullname = models.CharField(max_length=120)
    email = models.EmailField(max_length=100)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    birth = models.DateField()

    def __str__(self):
        return self.fullname

class Result(models.Model):
    candidate = models.ForeignKey(Candidate, related_name='candidate', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name='quiz', on_delete=models.CASCADE)
    result = models.CharField(max_length=10)

    def __str__(self):
        return self.result


