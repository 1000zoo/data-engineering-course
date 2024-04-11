from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from polls.models import *
from polls_api.serializers import *

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

class QuestionList(APIView):
    def get(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'POST'])
# def question_list(request):
#     if request.method == 'GET':
#         questions = Question.objects.all()
#         serializer = QuestionSerializer(questions, many=True)
#         return Response(serializer.data)
    
#     if request.method == 'POST':
#         serializer = QuestionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuestionDetail(APIView):
    def get(self, request, id):
        pass
    def put(self, request, id):
        pass
    def delete(self, request, id):
        pass

@api_view(["GET", "PUT", "DELETE"])
def question_detail(request, id):
    question = get_object_or_404(Question, pk=id)
    if request.method == "GET":
        serializer = QuestionSerializer(question)
        return Response(serializer.data)
    
    if request.method == "PUT":
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
