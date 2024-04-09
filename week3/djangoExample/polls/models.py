from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib import admin

class Question(models.Model):
    question_text = models.CharField(max_length=200, verbose_name="질문")
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="생성일")

    def __str__(self):
        return f'제목: {self.question_text}, 날짜: {self.pub_date}'
    
    @admin.display(boolean=True, description="최근 생성")
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f'[{self.question.question_text}] {self.choice_text}'
