from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from .models import Poll, Choice, Vote

# Create your tests here.
User = get_user_model()

def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

class PollsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='pass1234')
        self.user2 = User.objects.create_user(username='other', password='pass1234')
        self.client = APIClient()

    def test_create_poll_and_vote_flow(self):
        token = get_token_for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        create_data = {'title': 'Fav color?', 'choices': ['Red','Blue']}
        resp = self.client.post('/api/polls/', create_data, format='json')
        self.assertEqual(resp.status_code, 201)
        poll_id = resp.data.get('id')
        # Ensure choices created
        resp_detail = self.client.get(f'/api/polls/{poll_id}/')
        self.assertEqual(resp_detail.status_code, 200)
        choices = resp_detail.data.get('choices')
        self.assertTrue(len(choices) >= 2)
        choice_id = choices[0]['id']
        # Vote as other user
        token2 = get_token_for_user(self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token2}')
        vote_resp = self.client.post('/api/vote/', {'poll': poll_id, 'choice': choice_id}, format='json')
        self.assertEqual(vote_resp.status_code, 201)
        # Results show vote count
        results = self.client.get(f'/api/polls/{poll_id}/results/')
        self.assertEqual(results.status_code, 200)
        self.assertTrue('results' in results.data)

    def test_duplicate_vote_prevented(self):
        token = get_token_for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        poll = Poll.objects.create(title='Test', created_by=self.user)
        choice = Choice.objects.create(poll=poll, text='a')
        resp1 = self.client.post('/api/vote/', {'poll': poll.id, 'choice': choice.id}, format='json')
        self.assertEqual(resp1.status_code, 201)
        resp2 = self.client.post('/api/vote/', {'poll': poll.id, 'choice': choice.id}, format='json')
        self.assertIn(resp2.status_code, (400, 409))

    def test_vote_expired(self):
        token = get_token_for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        expired = timezone.now() - timezone.timedelta(days=1)
        poll = Poll.objects.create(title='Expired', created_by=self.user, expires_at=expired)
        choice = Choice.objects.create(poll=poll, text='x')
        resp = self.client.post('/api/vote/', {'poll': poll.id, 'choice': choice.id}, format='json')
        self.assertEqual(resp.status_code, 400)
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from .models import Poll, Choice, Vote

User = get_user_model()

def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

class PollsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='pass1234')
        self.user2 = User.objects.create_user(username='other', password='pass1234')
        self.client = APIClient()

    def test_create_poll_and_vote_flow(self):
        token = get_token_for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        create_data = {'title': 'Fav color?', 'choices': ['Red','Blue']}
        resp = self.client.post('/api/polls/', create_data, format='json')
        self.assertEqual(resp.status_code, 201)
        poll_id = resp.data.get('id')
        # Ensure choices created
        resp_detail = self.client.get(f'/api/polls/{poll_id}/')
        self.assertEqual(resp_detail.status_code, 200)
        choices = resp_detail.data.get('choices')
        self.assertTrue(len(choices) >= 2)
        choice_id = choices[0]['id']
        # Vote as other user
        token2 = get_token_for_user(self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token2}')
        vote_resp = self.client.post('/api/vote/', {'poll': poll_id, 'choice': choice_id}, format='json')
        self.assertEqual(vote_resp.status_code, 201)
        # Results show vote count
        results = self.client.get(f'/api/polls/{poll_id}/results/')
        self.assertEqual(results.status_code, 200)
        self.assertTrue('results' in results.data)

    def test_duplicate_vote_prevented(self):
        token = get_token_for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        poll = Poll.objects.create(title='Test', created_by=self.user)
        choice = Choice.objects.create(poll=poll, text='a')
        resp1 = self.client.post('/api/vote/', {'poll': poll.id, 'choice': choice.id}, format='json')
        self.assertEqual(resp1.status_code, 201)
        resp2 = self.client.post('/api/vote/', {'poll': poll.id, 'choice': choice.id}, format='json')
        self.assertIn(resp2.status_code, (400, 409))

    def test_vote_expired(self):
        token = get_token_for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        expired = timezone.now() - timezone.timedelta(days=1)
        poll = Poll.objects.create(title='Expired', created_by=self.user, expires_at=expired)
        choice = Choice.objects.create(poll=poll, text='x')
        resp = self.client.post('/api/vote/', {'poll': poll.id, 'choice': choice.id}, format='json')
        self.assertEqual(resp.status_code, 400)


