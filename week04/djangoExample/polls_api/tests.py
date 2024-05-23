from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone

from polls_api.serializers import *
from polls.models import *

class QuestionListTest(APITestCase):
    def setUp(self) -> None:
        self.question_data = {'question_text': "some question"}
        self.url = reverse('question-list')
    
    def test_create_question(self):
        user = User.objects.create(username='testuser', password='testpass')
        self.client.force_authenticate(user=user) ## 사용자 강제 로그인
        response = self.client.post(self.url, self.question_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 1)
        question = Question.objects.first()
        self.assertEqual(question.question_text, self.question_data['question_text'])
        self.assertLess((timezone.now() - question.pub_date).total_seconds(), 1)

    def test_create_question_without_authentication(self):
        response = self.client.post(self.url, self.question_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_questions(self):
        question1 = Question.objects.create(question_text="question1")
        choice1 = Choice.objects.create(question=question1, choice_text='choice1')
        question2 = Question.objects.create(question_text="question2")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 2)
        print(f"$$$$$$$$$$  {response.data}")


class VoteSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.question = Question.objects.create(
            question_text='abc',
            owner=self.user
        )
        self.choice = Choice.objects.create(
            question=self.question,
            choice_text="1"
        )

    def test_vote_serializer(self):
        data = {
            'question': self.question.id,
            'choice': self.choice.id,
            'voter': self.user.id
        }
        serializer = VoteSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        vote = serializer.save()
        self.assertEqual(vote.question, self.question)
        self.assertEqual(vote.choice, self.choice)
        self.assertEqual(vote.voter, self.user)

    def test_vote_serializer_with_duplicate_vote(self):
        choice1 = Choice.objects.create(
            question=self.question,
            choice_text="1"
        )
        Vote.objects.create(question=self.question, choice=choice1, voter=self.user)

        choice2 = Choice.objects.create(
            question=self.question,
            choice_text="2"
        )
        data = {
            'question': self.question.id,
            'choice': choice2.id,
            'voter': self.user.id
        }
        serialzier = VoteSerializer(data=data)
        self.assertFalse(serialzier.is_valid())


class QuestionSerializerTestCase(TestCase):
    def test_with_valid_data(self):
        serializer = QuestionSerializer(data={'question_text':"abc"})
        self.assertEqual(serializer.is_valid(), True)
        new_question = serializer.save()
        self.assertIsNotNone(new_question.id)

    def test_with_invalid_data(self):
        serializer = QuestionSerializer(data={'question_text':""})
        self.assertEqual(serializer.is_valid(), False)