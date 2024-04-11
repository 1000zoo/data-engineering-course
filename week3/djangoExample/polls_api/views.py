from django.shortcuts import render
from rest_framework.decorators import api_view
from polls.models import *
from polls_api.serializers import *

from rest_framework.response import Response

@api_view()
def question_list(request):
    questions = Question.objects.all()
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)
