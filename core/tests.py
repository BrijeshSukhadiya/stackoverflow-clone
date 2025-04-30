from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import CustomUser, Question, Answer, Vote

class StackOverflowCloneTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = CustomUser.objects.create_user(username='alice', email='alice@example.com', password='pass1234')
        self.user2 = CustomUser.objects.create_user(username='bob', email='bob@example.com', password='pass1234')

        self.question = Question.objects.create(
            author=self.user1,
            title='What is Django?',
            body='Explain Django framework.',
            tags='django,python'
        )

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_user_registration(self):
        response = self.client.post('/api/register/', {
            'username': 'charlie',
            'email': 'charlie@example.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_question(self):
        self.authenticate(self.user1)
        data = {
            'title': 'What is REST?',
            'body': 'Explain REST API in simple terms.',
            'tags': 'rest,api'
        }
        response = self.client.post('/api/questions/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_answer(self):
        self.authenticate(self.user2)
        data = {
            'question': self.question.id,
            'body': 'Django is a high-level Python web framework.'
        }
        response = self.client.post('/api/answers/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_accept_answer_and_notify(self):
        answer = Answer.objects.create(
            author=self.user2,
            question=self.question,
            body='Django is cool.'
        )
        self.authenticate(self.user1)
        url = f'/api/answers/{answer.id}/accept/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        answer.refresh_from_db()
        self.assertTrue(answer.is_accepted)

    def test_upvote_question(self):
        self.authenticate(self.user2)
        data = {
            'model': 'question',
            'id': self.question.id,
            'vote': 1
        }
        response = self.client.post('/api/vote/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        vote = Vote.objects.get(object_id=self.question.id, user=self.user2)
        self.assertEqual(vote.vote, 1)

    def test_downvote_answer(self):
        answer = Answer.objects.create(
            author=self.user2,
            question=self.question,
            body='Sample answer'
        )
        self.authenticate(self.user1)
        data = {
            'model': 'answer',
            'id': answer.id,
            'vote': -1
        }
        response = self.client.post('/api/vote/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        vote = Vote.objects.get(object_id=answer.id, user=self.user1)
        self.assertEqual(vote.vote, -1)

    def test_view_profile(self):
        self.authenticate(self.user1)
        response = self.client.get('/api/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'alice')
