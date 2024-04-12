from django.test import TestCase
from django.contrib.auth.models import User

from polls_api.serializers import *
from polls.models import *

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