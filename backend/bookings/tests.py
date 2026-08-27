from datetime import timedelta
from django.utils import timezone
from django.test import TransactionTestCase
from django.db import connections, close_old_connections
from rest_framework.test import APITestCase, APIClient
from threading import Barrier, Thread
from users.models import User
from sessions_app.models import Session
from .models import Booking

class BookingTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u', email='u@example.com', password='x')
        creator = User.objects.create_user(username='c', email='c@example.com', password='x', role='CREATOR')
        self.session = Session.objects.create(creator=creator, title='Future', description='x', start_time=timezone.now()+timedelta(days=1), duration_minutes=30, capacity=1)
        self.client.force_authenticate(self.user)
    def test_duplicate_active_booking_conflicts(self):
        self.assertEqual(self.client.post(f'/api/sessions/{self.session.id}/book/').status_code, 201)
        self.assertEqual(self.client.post(f'/api/sessions/{self.session.id}/book/').status_code, 409)
    def test_started_session_conflicts(self):
        self.session.start_time = timezone.now()-timedelta(minutes=1); self.session.save()
        self.assertEqual(self.client.post(f'/api/sessions/{self.session.id}/book/').status_code, 409)
    def test_booking_list_represents_upcoming_and_past_sessions(self):
        past = Session.objects.create(creator=self.session.creator, title='Past', description='x', start_time=timezone.now()-timedelta(days=1), duration_minutes=30, capacity=1)
        self.client.post(f'/api/sessions/{self.session.id}/book/')
        Booking.objects.create(user=self.user, session=past)
        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, 200)
        start_times = {item['session']['start_time'] for item in response.data}
        self.assertIn(self.session.start_time.isoformat().replace('+00:00', 'Z'), start_times)
        self.assertIn(past.start_time.isoformat().replace('+00:00', 'Z'), start_times)

    def test_creator_dashboard_reports_own_active_booking_counts(self):
        other_creator = User.objects.create_user(username='other', email='other@example.com', password='x', role='CREATOR')
        other_session = Session.objects.create(creator=other_creator, title='Other', description='x', start_time=timezone.now()+timedelta(days=1), duration_minutes=30, capacity=1)
        self.client.post(f'/api/sessions/{self.session.id}/book/')
        Booking.objects.create(user=other_creator, session=other_session)
        self.client.force_authenticate(self.session.creator)
        response = self.client.get('/api/creator/sessions/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.session.id)
        self.assertEqual(response.data[0]['active_booking_count'], 1)

class BookingConcurrencyTests(TransactionTestCase):
    """TransactionTestCase is required: each thread needs a real DB transaction."""
    reset_sequences = True
    def test_capacity_one_allows_exactly_one_concurrent_booking(self):
        creator = User.objects.create_user(username='creator', email='creator@example.com', password='x', role='CREATOR')
        session = Session.objects.create(creator=creator, title='Race', description='x', start_time=timezone.now()+timedelta(days=1), duration_minutes=30, capacity=1)
        users = [User.objects.create_user(username=f'u{i}', email=f'u{i}@example.com', password='x') for i in range(2)]
        barrier, results = Barrier(2), []
        def book(user):
            # A thread owns its Django connection; explicitly close it so the
            # PostgreSQL test database can be dropped during test teardown.
            close_old_connections()
            try:
                client = APIClient()
                client.force_authenticate(user=user)
                barrier.wait()
                results.append(client.post(f'/api/sessions/{session.id}/book/').status_code)
            finally:
                connections['default'].close()
        threads = [Thread(target=book, args=(user,)) for user in users]
        [thread.start() for thread in threads]; [thread.join() for thread in threads]
        self.assertEqual(sorted(results), [201, 409])
        self.assertEqual(Booking.objects.filter(session=session, status=Booking.Status.ACTIVE).count(), 1)
