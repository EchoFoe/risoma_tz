from django.urls import path
from .views import PostListView, PostDetailView

app_name = 'api_blogs'

urlpatterns = [
    path('post-list/', PostListView.as_view(), name='posts-list'),
    path('post-detail/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
]
