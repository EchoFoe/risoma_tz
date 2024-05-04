from typing import Type, Any, Optional

from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination, BasePagination
from rest_framework import status
from rest_framework.response import Response

from django.db.models.query import QuerySet

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.serializers import BaseSerializer

from blogs.models import Post
from .serializers import PostSerializer

POSTS = 'Посты'


class PostPagination(PageNumberPagination):
    page_size = 10


class PostListView(ListAPIView):
    """
    Список постов.

    Параметры запроса:
    - page (int): Номер страницы.
    - blog_id (int): Идентификатор блога.

    Пример ответа:
    Если посты найдены, возвращается статус 200 OK и список постов:
    - [
        {
            "id": "Идентификатор поста (int)",
            "blog": {
                "id": "Идентификатор блога (int)",
                "account": {
                    "username": "Логин автора блога (str)",
                    "phone": "Номер телефона автора блога (str)",
                    "full_name": "Фамилия и имя автора блога (str)"
                }
            },
            "title": "Заголовок поста (str)",
            "content": "Содержание поста (str)",
            "num_comments": "Количество комментариев (int)",
            "is_active": true (bool),
            "created_at": "Дата и время создания поста (str)",
            "updated_at": "Дата и время обновления поста (str)"
        },
        ...
    ]
    Если постов не найдено, возвращается пустой список.
    """

    queryset: QuerySet[Post] = Post.objects.filter(is_active=True)
    serializer_class: Type[BaseSerializer] = PostSerializer
    pagination_class: Type[BasePagination] = PostPagination

    @swagger_auto_schema(
        tags=[POSTS],
        operation_summary='Список постов',
        responses={200: openapi.Response('OK', PostSerializer(many=True))},
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, description='Номер страницы', type=openapi.TYPE_INTEGER),
            openapi.Parameter('blog_id', openapi.IN_QUERY, description='Идентификатор блога для фильтрации постов',
                              type=openapi.TYPE_INTEGER),
        ]
    )
    def get(self, request, *args, **kwargs) -> Response:
        try:
            queryset: QuerySet[Post] = self.get_queryset()
            blog_id: Optional[int] = request.query_params.get('blog_id')
            page_size: int = int(request.query_params.get('page_size', self.pagination_class.page_size))
            if blog_id is not None:
                queryset = queryset.filter(blog__id=blog_id)
            self.pagination_class.page_size = page_size
            page: Any = self.paginate_queryset(queryset)
            if page is not None:
                serializer: Any = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer: Any = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
