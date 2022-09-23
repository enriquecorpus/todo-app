import django.forms
import todolist.models


class TodoListForm(django.forms.ModelForm):
    title = django.forms.CharField(max_length=100, required=True)
    description = django.forms.CharField(widget=django.forms.Textarea, required=False)
    author = django.forms.CharField(widget=django.forms.HiddenInput(), required=False)

    def __init__(self, author, *args, **kwargs):
        super(TodoListForm, self).__init__(*args, **kwargs)
        self.author = author

    class Meta:
        model = todolist.models.TodoList
        exclude = ['created_at', 'updated_at', 'deleted_at']

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise django.forms.ValidationError('Title must be at least 5 characters long')
        if len(title) > 100:
            raise django.forms.ValidationError('Title must not be 100 characters long')
        return title

    def clean_description(self):
        description = self.cleaned_data['description']
        if len(description) > 2000:
            raise django.forms.ValidationError('Description must not be 2000 characters long')
        return description

    def clean_author(self):
        if self.instance and self.instance.pk and self.instance.author != self.author:
            raise django.forms.ValidationError('You are not the author of this todo item')
        return self.author

    def save(self, commit=True):
        return super(TodoListForm, self).save(commit=commit)