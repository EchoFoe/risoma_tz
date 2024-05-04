from rest_framework import serializers

from blogs.models import Post, Blog, Comment
from accounts.models import Account


class AuthorSerializer(serializers.ModelSerializer):
    """ Сериализатор для юзеров. """

    full_name = serializers.CharField(source='get_full_name')

    class Meta:
        model = Account
        fields = ['username', 'phone', 'full_name']


class BlogSerializer(serializers.ModelSerializer):
    """ Сериализатор для юлога. """

    account = AuthorSerializer(source='user', read_only=True)

    class Meta:
        model = Blog
        fields = ['id', 'account']


class PostSerializer(serializers.ModelSerializer):
    """ Сериализатор для постов. """

    num_comments = serializers.SerializerMethodField(read_only=True)
    author = AuthorSerializer(read_only=True)
    blog = BlogSerializer(read_only=True)
    created_at = serializers.DateTimeField(format='%d.%m.%Y %H:%M:%S')
    updated_at = serializers.DateTimeField(format='%d.%m.%Y %H:%M:%S')

    class Meta:
        model = Post
        fields = ['id', 'blog', 'author', 'title', 'content', 'num_comments', 'is_active', 'created_at', 'updated_at']

    def get_num_comments(self, post):
        return post.comments.filter(is_active=True).count()


class CommentSerializer(serializers.ModelSerializer):
    """ Сериализатор для комментариев. """

    author = AuthorSerializer(read_only=True)
    created_at = serializers.DateTimeField(format='%d.%m.%Y %H:%M:%S')
    updated_at = serializers.DateTimeField(format='%d.%m.%Y %H:%M:%S')

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'created_at', 'updated_at')
