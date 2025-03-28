from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import timedelta
from .models import Activity, ActivityCategory, ActivityReview

class ActivityTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = ActivityCategory.objects.create(
            name='Adventure',
            description='Adventure activities'
        )
        self.activity = Activity.objects.create(
            name='Mountain Hiking',
            category=self.category,
            description='Exciting mountain hiking experience',
            location='Mont Blanc',
            duration=timedelta(hours=4),
            difficulty='intermediate',
            min_participants=2,
            max_participants=10,
            price=50.00,
            fitness_level=3
        )

    def test_list_activities(self):
        response = self.client.get('/api/activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_activity(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'name': 'Scuba Diving',
            'category_id': self.category.id,
            'description': 'Deep sea diving experience',
            'location': 'Great Barrier Reef',
            'duration': '02:00:00',
            'difficulty': 'advanced',
            'min_participants': 1,
            'max_participants': 4,
            'price': 100.00,
            'fitness_level': 4
        }
        response = self.client.post('/api/activities/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_review(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'rating': 5,
            'comment': 'Amazing experience!'
        }
        response = self.client.post(
            f'/api/activities/{self.activity.id}/add_review/',
            data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.activity.refresh_from_db()
        self.assertEqual(self.activity.rating, 5.0)

    def test_similar_activities(self):
        Activity.objects.create(
            name='Rock Climbing',
            category=self.category,
            description='Rock climbing experience',
            location='Alps',
            duration=timedelta(hours=3),
            difficulty='advanced',
            min_participants=1,
            max_participants=5,
            price=75.00,
            fitness_level=4
        )
        response = self.client.get(f'/api/activities/{self.activity.id}/similar_activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
