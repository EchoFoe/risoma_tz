from dal import autocomplete

from django.db.models import Q

from accounts.models import Account
from blogs.models import Blog, Post


class AdminPostAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if self.q:
            return Post.objects.filter(title__icontains=self.q)
        else:
            return Post.objects.filter(is_active=True)


class AdminBlogAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if self.q:
            return Blog.objects.filter(Q(user__last_name__icontains=self.q) | Q(user__first_name__icontains=self.q))
        else:
            return Blog.objects.filter(is_active=True)


class AdminUserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if self.q:
            return Account.objects.filter(Q(last_name__icontains=self.q) | Q(first_name__icontains=self.q))
        else:
            return Account.objects.all()
