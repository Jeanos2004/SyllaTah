from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import BlogPost, Category, Tag

class BlogTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Test Category')
        self.tag = Tag.objects.create(name='Test Tag')
        self.post = BlogPost.objects.create(
            title='Test Post',
            content='Test Content',
            author=self.user,
            category=self.category,
            status='published'
        )
        self.post.tags.add(self.tag)

    def test_list_posts(self):
        response = self.client.get('/api/blog/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Post',
            'content': 'New Content',
            'category_id': self.category.id,
            'tag_ids': [self.tag.id],
            'status': 'published'
        }
        response = self.client.post('/api/blog/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
