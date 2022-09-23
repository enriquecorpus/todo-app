from django.shortcuts import render
import django.contrib.auth.decorators
import todolist.models


@django.contrib.auth.decorators.login_required
def index(request):
    todos = todolist.models.TodoList.objects.filter(author=request.user)
    return render(request=request, template_name="todolist/index.html", context={"todolist": todos})

