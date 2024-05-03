from django.urls import path
from blogs.filters.autocomplete_light_registry import AdminBlogAutocomplete, AdminPostAutocomplete, \
    AdminUserAutocomplete

app_name = 'blogs'

urlpatterns = [
    path('admin_blog_autocomplete/', AdminBlogAutocomplete.as_view(), name='admin_blog_autocomplete'),
    path('admin_post_autocomplete/', AdminPostAutocomplete.as_view(), name='admin_post_autocomplete'),
    path('admin_user_autocomplete/', AdminUserAutocomplete.as_view(), name='admin_user_autocomplete'),
]
