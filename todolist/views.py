from django.shortcuts import render
import django.contrib.auth.decorators
import todolist.models
import utils.ajax
import django.views.decorators.http
import django.http
import django.urls
from django.shortcuts import render, redirect
from django.contrib import messages


@django.contrib.auth.decorators.login_required
def index(request):
    todos = todolist.models.TodoList.objects.filter(author=request.user)
    return render(request=request, template_name="todolist/index.html", context={"todolist": todos})


@django.contrib.auth.decorators.login_required
@django.views.decorators.http.require_http_methods(["POST"])
@utils.ajax.ajax_required
def remove_todo(request):
    try:
        todo_id = request.POST["todo_id"]
        todo = todolist.models.TodoList.objects.get(id=todo_id)
        if todo.author != request.user:
            return django.http.HttpResponseForbidden()
        todo.delete()
        return django.http.JsonResponse({"status": "ok"})
    except KeyError:
        return django.http.HttpResponseBadRequest()
    except todolist.models.TodoList.DoesNotExist:
        return django.http.HttpResponseNotFound()


@django.contrib.auth.decorators.login_required
@django.views.decorators.http.require_http_methods(["POST"])
def add_comment(request):
    try:
        todo = todolist.models.TodoList.objects.get(id=request.POST.get("todo_id"))
        if todo.author != request.user:
            messages.error(request, "You are not authorized to add comment to this todo.")
        comment = todolist.models.Comments()
        comment.author = request.user
        comment.todo = todo
        comment.comment = request.POST["comment"]
        comment.save()
    except todolist.models.TodoList.DoesNotExist:
        messages.error(request, "Todo does not exist.")
    except KeyError:
        messages.error(request, "Comment is required.")
    return redirect("index")


@django.contrib.auth.decorators.login_required
@django.views.decorators.http.require_http_methods(["POST"])
@utils.ajax.ajax_required
def remove_comment(request):
    try:
        comment = todolist.models.Comments.objects.get(id=request.POST["comment_id"])
        if comment.author != request.user:
            return django.http.HttpResponseForbidden()
        comment.delete()
        return django.http.JsonResponse({"status": "ok"})
    except KeyError:
        return django.http.HttpResponseBadRequest()
    except todolist.models.Comments.DoesNotExist:
        return django.http.HttpResponseNotFound()