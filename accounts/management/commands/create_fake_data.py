from typing import Any
from tqdm import tqdm
import random

from django.db import transaction
from django.core.management.base import BaseCommand

from accounts.models import Account
from accounts.factories import UserFactory
from blogs.factories import BlogFactory


class Command(BaseCommand):
    help: str = 'Создание фейковых данных'

    def add_arguments(self, parser: Any) -> None:
        parser.add_argument('--num_users', type=int, default=50, help='Кол-во пользователей')
        parser.add_argument('--num_blogs_per_user', type=int, default=1, help='Кол-во блогов для каждого пользователя')
        parser.add_argument('--num_posts_per_blog', type=int, default=3, help='Кол-во постов для каждого блога')
        parser.add_argument(
            '--num_comments_per_post', type=int, default=5, help='Кол-во комментариев для каждого поста'
        )

    def handle(self, *args: Any, **kwargs: Any) -> None:
        num_users: int = kwargs['num_users']
        num_blogs_per_user: int = kwargs['num_blogs_per_user']
        num_posts_per_blog: int = kwargs['num_posts_per_blog']
        num_comments_per_post: int = kwargs['num_comments_per_post']

        self.stdout.write('Создание тестовых данных...')
        with tqdm(total=num_users, desc='Пользователи') as pbar_data:
            with transaction.atomic():
                try:
                    for _ in range(num_users):
                        user: Account = UserFactory.create_fake_user()
                        pbar_data.update(1)

                        for _ in range(min(num_blogs_per_user, 1)):
                            blog = BlogFactory.create_fake_blog(user)

                            for _ in range(num_posts_per_blog):
                                post = BlogFactory.create_fake_post(blog)

                                for _ in range(num_comments_per_post):
                                    random_user = random.choice(Account.objects.exclude(pk=user.pk))
                                    BlogFactory.create_fake_comment(post, random_user)
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Произошла ошибка: {e}'))
                    return

        self.stdout.write(self.style.SUCCESS('Готово!'))
