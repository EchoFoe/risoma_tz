from typing import List

from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient

from blogs.factories import BlogFactory
from blogs.models import Blog, Post
from accounts.factories import UserFactory
from accounts.models import Account


class PostListViewTestCase(TestCase):
    """Тестирование представления для списка постов."""

    def setUp(self) -> None:
        """Настройка тестовых данных."""

        self.client: APIClient = APIClient()
        self.user: Account = UserFactory.create_fake_user()
        self.api_url: str = reverse('api_blogs:posts-list')
        self.blog: Blog = BlogFactory.create_fake_blog(user=self.user)
        self.posts: List[Post] = [BlogFactory.create_fake_post(blog=self.blog) for _ in range(15)]

    def test_list_posts(self) -> None:
        """Тестирование получения списка постов и структуры данных"""

        response = self.client.get(self.api_url)
        self.assertEqual(response.status_code, 200)

        self.assertIn('results', response.data)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)

        self.assertEqual(len(response.data['results']), 10)
