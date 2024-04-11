from rest_framework import serializers
from polls.models import *

from django.contrib.auth.models import User

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "question_text", "pub_date"]

class UserSerializer(serializers.ModelSerializer):
    questions = serializers.PrimaryKeyRelatedField(many=True, queryset=Question.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'questions']