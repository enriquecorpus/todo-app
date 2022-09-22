import django.forms
import models


class TodoListForm(django.forms.Form):
    title = django.forms.CharField(max_length=100, required=True)
    description = django.forms.CharField(widget=django.forms.Textarea, required=False)
    author = django.forms.Field(required=True)

    class Meta:
        model = models.TodoList
        exclude = ['author', 'created_at', 'updated_at', 'deleted_at']

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise django.forms.ValidationError('Title must be at least 5 characters long')
        if len(title) > 100:
            raise django.forms.ValidationError('Title must not be 100 characters long')
        return title

    def clean_author(self):
        try:
            author = self.cleaned_data['author']
            author = models.MyUser.objects.get(username=author)
            if not author:
                raise django.forms.ValidationError('Author must be set')
            return author
        except models.MyUser.DoesNotExist:
            raise django.forms.ValidationError('Author must be set')