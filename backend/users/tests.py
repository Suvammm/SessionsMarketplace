from datetime import timedelta
from django.core.management import call_command
from django.utils import timezone
from rest_framework.test import APITestCase
from .models import User

class AuthTests(APITestCase):
    def test_invalid_jwt_is_unauthorized(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid')
        self.assertEqual(self.client.get('/api/auth/me/').status_code, 401)

    def test_new_user_can_select_user_role_once(self):
        user = User.objects.create_user(username='new-user', email='new-user@example.com', password='x')
        self.client.force_authenticate(user)
        response = self.client.post('/api/auth/role/', {'role': 'USER'}, format='json')
        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertTrue(user.role_selected)
        self.assertEqual(user.role, User.Role.USER)

    def test_new_user_can_select_creator_role_once(self):
        user = User.objects.create_user(username='new-creator', email='new-creator@example.com', password='x')
        self.client.force_authenticate(user)
        self.assertEqual(self.client.post('/api/auth/role/', {'role': 'CREATOR'}, format='json').status_code, 200)
        self.assertEqual(self.client.post('/api/auth/role/', {'role': 'USER'}, format='json').status_code, 409)
        user.refresh_from_db()
        self.assertEqual(user.role, User.Role.CREATOR)

    def test_profile_cannot_change_role(self):
        user = User.objects.create_user(username='profile-user', email='profile@example.com', password='x')
        self.client.force_authenticate(user)
        self.assertEqual(self.client.patch('/api/auth/profile/', {'role': 'CREATOR'}, format='json').status_code, 200)
        user.refresh_from_db()
        self.assertEqual(user.role, User.Role.USER)

class DemoLoginTests(APITestCase):
    def setUp(self):
        call_command('create_demo_users')

    def login(self, username, password):
        return self.client.post('/api/auth/login/', {'username': username, 'password': password}, format='json')

    def test_demo_user_receives_jwt_and_user_role(self):
        response = self.login('demo_user', 'demo_user_password')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['user']['role'], User.Role.USER)

    def test_demo_creator_receives_jwt_and_creator_role(self):
        response = self.login('demo_creator', 'demo_creator_password')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['user']['role'], User.Role.CREATOR)

    def test_invalid_demo_password_is_unauthorized(self):
        self.assertEqual(self.login('demo_user', 'wrong-password').status_code, 401)

    def test_demo_user_cannot_create_session(self):
        response = self.login('demo_user', 'demo_user_password')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        response = self.client.post('/api/sessions/', {'title':'x','description':'x','start_time':(timezone.now()+timedelta(days=1)).isoformat(),'duration_minutes':30,'capacity':1}, format='json')
        self.assertEqual(response.status_code, 403)

    def test_demo_creator_can_create_session(self):
        response = self.login('demo_creator', 'demo_creator_password')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        response = self.client.post('/api/sessions/', {'title':'x','description':'x','start_time':(timezone.now()+timedelta(days=1)).isoformat(),'duration_minutes':30,'capacity':1}, format='json')
        self.assertEqual(response.status_code, 201)
