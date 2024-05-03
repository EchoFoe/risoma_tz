from django.db import models

from .bases import DateTimeBaseModel


class Blog(DateTimeBaseModel):
    user = models.OneToOneField('accounts.Account', on_delete=models.CASCADE, related_name='blog', db_index=True,
                                verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'

    def __str__(self):
        return f'Блог пользователя: {self.user.username}'


class Post(DateTimeBaseModel):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='posts', db_index=True, verbose_name='Блог')
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    content = models.TextField(max_length=140, blank=True, verbose_name='Текст', help_text='Не более 140 символов')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return f'{self.title}'


class Comment(DateTimeBaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Пост')
    author = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, verbose_name='Автор комментария')
    text = models.TextField(
        max_length=200, blank=True, verbose_name='Текст комментария', help_text='Не более 200 символов'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий от {self.author.username} к посту "{self.post.title}"'
