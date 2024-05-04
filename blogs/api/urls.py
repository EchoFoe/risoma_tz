from django.urls import path
from .views import PostListView

app_name = 'api_blogs'

urlpatterns = [
    path('post-list/', PostListView.as_view(), name='posts-list'),
]
