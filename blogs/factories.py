from django.utils import timezone
from faker import Faker

from accounts.models import Account

from .models import Blog, Post, Comment

fake = Faker()


class BlogFactory:
    @staticmethod
    def create_fake_blog(user: Account) -> Blog:
        """Создает блог для пользователя."""
        return Blog.objects.create(user=user)

    @staticmethod
    def create_fake_post(blog: Blog) -> Post:
        """Создает пост для блога."""
        return Post.objects.create(
            blog=blog,
            title=fake.sentence()[:100],
            content=fake.text(max_nb_chars=140),
            created_at=timezone.now()
        )

    @staticmethod
    def create_fake_comment(post: Post, user: Account) -> Comment:
        """Создает комментарий для поста."""
        return Comment.objects.create(
            post=post,
            author=user,
            text=fake.text(max_nb_chars=200),
            created_at=timezone.now()
        )
