from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from polls.models import *
from polls_api.serializers import *

from rest_framework.response import Response
from rest_framework import status, mixins, generics
from rest_framework.views import APIView

class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
        
class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer



