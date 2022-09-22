import django.db.models
import accounts.models


class TodoList(django.db.models.Model):
    title = django.db.models.CharField(max_length=100)
    description = django.db.models.TextField(null=True, blank=True)
    author = django.db.models.ForeignKey(accounts.models.MyUser, on_delete=django.db.models.CASCADE)
    created_at = django.db.models.DateTimeField(auto_now_add=True)
    updated_at = django.db.models.DateTimeField(auto_now=True)
    deleted_at = django.db.models.DateTimeField(null=True, default=None)


class Comments(django.db.models.Model):
    todo = django.db.models.ForeignKey(TodoList, on_delete=django.db.models.CASCADE)
    comment = django.db.models.TextField()
    author = django.db.models.ForeignKey(accounts.models.MyUser, on_delete=django.db.models.CASCADE)
    created_at = django.db.models.DateTimeField(auto_now_add=True)
    updated_at = django.db.models.DateTimeField(auto_now=True)
    deleted_at = django.db.models.DateTimeField(null=True, default=None)
