from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Transport, TransportCategory, TransportReview

class TransportTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = TransportCategory.objects.create(
            name='Test Category',
            description='Test Description'
        )
        self.transport = Transport.objects.create(
            company_name='Test Company',
            transport_type='Test Type',
            category=self.category,
            vehicle_type='Test Vehicle',
            capacity=4,
            luggage_capacity=2,
            price=100.00,
            description='Test Description'
        )

    def test_list_transports(self):
        response = self.client.get('/api/transports/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_transport(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'company_name': 'New Company',
            'transport_type': 'New Type',
            'category_id': self.category.id,
            'vehicle_type': 'New Vehicle',
            'capacity': 6,
            'luggage_capacity': 3,
            'price': 150.00,
            'description': 'New Description'
        }
        response = self.client.post('/api/transports/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_review(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'rating': 5,
            'comment': 'Great service!'
        }
        response = self.client.post(
            f'/api/transports/{self.transport.id}/add_review/',
            data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.transport.refresh_from_db()
        self.assertEqual(self.transport.rating, 5.0)
