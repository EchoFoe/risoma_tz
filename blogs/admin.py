from typing import Any

from django.contrib import admin
from django.db.models import Field
from django.urls import reverse
from django.http import HttpRequest

from dal import autocomplete

from .models import Blog, Post, Comment


class PostInline(admin.StackedInline):
    """ Класс-хелпер для отображения объектов Post, связанных с Blog """

    model = Post
    extra = 1
    verbose_name_plural = 'Посты к блогу'
    verbose_name = 'Пост к блогу'
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Заголовок', {'fields': (('title', 'is_active'),)}),
        ('Контент поста', {'fields': ('content',)}),
        ('Даты', {'fields': (('created_at', 'updated_at'),)}),
    )


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    """ Админ-панель для Blog """

    def formfield_for_foreignkey(self, db_field: Field, request: HttpRequest, **kwargs: Any) -> Any:
        """
        Переопределение поля формы для внешнего ключа.

        :param db_field: Обрабатываемое поле базы данных.
        :type db_field: Field.
        :param request: Текущий HTTP-запрос.
        :type request: HttpRequest.
        :param kwargs: Именованные аргументы.
        :type kwargs: Any

        :return: Измененное поле формы.
        :rtype: Any
        """
        if db_field.name == 'user':
            kwargs['widget'] = autocomplete.ModelSelect2(url=reverse('blogs:admin_user_autocomplete'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    save_as = True
    inlines = [PostInline]
    readonly_fields = ['created_at', 'updated_at']
    list_display = ['id', 'user', 'is_active']
    list_filter = ['is_active']
    list_display_links = ['id']
    list_per_page = 50
    search_fields = ['user', 'id']
    fieldsets = (
        ('Основная информация', {'fields': (('user', 'is_active'),)}),
        ('Даты', {'fields': (('created_at', 'updated_at'),)}),
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """ Админ-панель для Blog """

    def formfield_for_foreignkey(self, db_field: Field, request: HttpRequest, **kwargs: Any) -> Any:
        """
        Переопределение поля формы для внешнего ключа.

        :param db_field: Обрабатываемое поле базы данных.
        :type db_field: Field.
        :param request: Текущий HTTP-запрос.
        :type request: HttpRequest.
        :param kwargs: Именованные аргументы.
        :type kwargs: Any

        :return: Измененное поле формы.
        :rtype: Any
        """
        if db_field.name == 'blog':
            kwargs['widget'] = autocomplete.ModelSelect2(url=reverse('blogs:admin_blog_autocomplete'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    save_as = True
    readonly_fields = ['created_at', 'updated_at']
    list_display = ['id', 'blog', 'title']
    list_filter = ['is_active']
    list_display_links = ['id']
    list_per_page = 50
    search_fields = ['blog', 'title']
    fieldsets = (
        ('Основная информация', {'fields': (('title', 'blog', 'is_active'),)}),
        ('Контент', {'fields': ('content',)}),
        ('Даты', {'fields': (('created_at', 'updated_at'),)}),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """ Админ-панель для Comment """

    def formfield_for_foreignkey(self, db_field: Field, request: HttpRequest, **kwargs: Any) -> Any:
        """
        Переопределение поля формы для внешнего ключа.

        :param db_field: Обрабатываемое поле базы данных.
        :type db_field: Field.
        :param request: Текущий HTTP-запрос.
        :type request: HttpRequest.
        :param kwargs: Именованные аргументы.
        :type kwargs: Any

        :return: Измененное поле формы.
        :rtype: Any
        """
        if db_field.name == 'post':
            kwargs['widget'] = autocomplete.ModelSelect2(url=reverse('blogs:admin_post_autocomplete'))
        if db_field.name == 'author':
            kwargs['widget'] = autocomplete.ModelSelect2(url=reverse('blogs:admin_user_autocomplete'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    save_as = True
    readonly_fields = ['created_at', 'updated_at']
    list_display = ['id', 'post', 'author']
    list_filter = ['is_active']
    list_display_links = ['id']
    list_per_page = 50
    search_fields = ['author', 'post__title']
    fieldsets = (
        ('Основная информация', {'fields': (('post', 'author', 'is_active'),)}),
        ('Текст комментария', {'fields': ('text',)}),
        ('Даты', {'fields': (('created_at', 'updated_at'),)}),
    )
