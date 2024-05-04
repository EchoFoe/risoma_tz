from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient

from accounts.factories import UserFactory
from accounts.models import Account
from blogs.factories import BlogFactory
from blogs.models import Blog, Post


class PostDetailViewTestCase(TestCase):
    """Тестирование представления для деталей поста."""

    def setUp(self):
        """Настройка тестовых данных."""

        self.client: APIClient = APIClient()
        self.user: Account = UserFactory.create_fake_user()
        self.blog: Blog = BlogFactory.create_fake_blog(user=self.user)
        self.post: Post = BlogFactory.create_fake_post(blog=self.blog)
        self.api_url: str = reverse('api_blogs:post-detail', kwargs={'pk': self.post.id})

    def test_retrieve_post_detail(self):
        """Тестирование получения деталей поста и его структуры ответа """

        for _ in range(3):
            BlogFactory.create_fake_comment(post=self.post, user=self.user)

        response = self.client.get(self.api_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.post.id)
        self.assertEqual(response.data['title'], self.post.title)
        self.assertEqual(response.data['content'], self.post.content)
        self.assertEqual(response.data['num_comments'], self.post.comments.count())

        self.assertEqual(response.data['blog']['id'], self.post.blog.id)
        self.assertEqual(response.data['blog']['account']['username'], self.user.username)
        self.assertEqual(response.data['blog']['account']['phone'], self.user.phone)
        self.assertEqual(response.data['blog']['account']['full_name'], self.user.get_full_name())

        for comment_data, comment in zip(response.data['comments'], self.post.comments.all()):
            self.assertEqual(comment_data['id'], comment.id)
            self.assertEqual(comment_data['text'], comment.text)
            self.assertEqual(comment_data['author']['username'], self.user.username)
            self.assertEqual(comment_data['author']['phone'], self.user.phone)
            self.assertEqual(comment_data['author']['full_name'], self.user.get_full_name())
