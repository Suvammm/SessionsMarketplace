from datetime import timedelta
from django.utils import timezone
from rest_framework.test import APITestCase
from users.models import User
from .models import Session

class AuthorizationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u', email='u@example.com', password='x')
        self.a = User.objects.create_user(username='a', email='a@example.com', password='x', role='CREATOR')
        self.b = User.objects.create_user(username='b', email='b@example.com', password='x', role='CREATOR')
    def test_user_cannot_create_session(self):
        self.client.force_authenticate(self.user)
        response = self.client.post('/api/sessions/', {'title':'x','description':'x','start_time':(timezone.now()+timedelta(days=1)).isoformat(),'duration_minutes':30,'capacity':1}, format='json')
        self.assertEqual(response.status_code, 403)
    def test_creator_can_create_session(self):
        self.client.force_authenticate(self.a)
        response = self.client.post('/api/sessions/', {'title':'x','description':'x','start_time':(timezone.now()+timedelta(days=1)).isoformat(),'duration_minutes':30,'capacity':1}, format='json')
        self.assertEqual(response.status_code, 201)
    def test_creator_cannot_edit_another_session(self):
        session = Session.objects.create(creator=self.b, title='x', description='x', start_time=timezone.now()+timedelta(days=1), duration_minutes=30, capacity=1)
        self.client.force_authenticate(self.a)
        self.assertEqual(self.client.patch(f'/api/sessions/{session.id}/', {'title':'bad'}, format='json').status_code, 403)
    def test_creator_cannot_delete_another_session(self):
        session = Session.objects.create(creator=self.b, title='x', description='x', start_time=timezone.now()+timedelta(days=1), duration_minutes=30, capacity=1)
        self.client.force_authenticate(self.a)
        self.assertEqual(self.client.delete(f'/api/sessions/{session.id}/').status_code, 403)
