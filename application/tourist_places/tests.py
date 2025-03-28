from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import TouristPlace, Region, PlaceReview

class TouristPlaceTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.region = Region.objects.create(
            name='Paris',
            description='Capital of France'
        )
        self.place = TouristPlace.objects.create(
            name='Eiffel Tower',
            description='Famous landmark',
            region=self.region,
            place_type='historical',
            address='Champ de Mars, Paris',
            best_visit_time='Evening',
            entrance_fee=25.00
        )

    def test_list_places(self):
        response = self.client.get('/api/tourist-places/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_place(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'name': 'Notre-Dame',
            'description': 'Historic cathedral',
            'region_id': self.region.id,
            'place_type': 'religious',
            'address': 'Île de la Cité, Paris',
            'best_visit_time': 'Morning',
            'entrance_fee': 0.00
        }
        response = self.client.post('/api/tourist-places/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_review(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'rating': 5,
            'comment': 'Magnificent view!',
            'visit_date': '2023-12-01'
        }
        response = self.client.post(
            f'/api/tourist-places/{self.place.id}/add_review/',
            data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.place.refresh_from_db()
        self.assertEqual(self.place.rating, 5.0)

    def test_nearby_places(self):
        TouristPlace.objects.create(
            name='Arc de Triomphe',
            description='Historic monument',
            region=self.region,
            place_type='historical',
            address='Place Charles de Gaulle, Paris',
            best_visit_time='Afternoon'
        )
        response = self.client.get(f'/api/tourist-places/{self.place.id}/nearby_places/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
