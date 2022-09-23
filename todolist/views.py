from django.shortcuts import render
import django.contrib.auth.decorators
import todolist.models
import utils.ajax
import django.views.decorators.http
import django.http
import django.urls
from django.shortcuts import render, redirect
from django.contrib import messages
import todolist.forms


@django.contrib.auth.decorators.login_required
def index(request):
    todos = todolist.models.TodoList.objects.filter(author=request.user)
    if request.method == "POST":
        instance = None
        todo_id = request.POST.get("update_todo_id")
        if todo_id:
            instance = todolist.models.TodoList.objects.get(id=todo_id)
        form = todolist.forms.TodoListForm(request.user, request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("index")
        for error in form.errors:
            for err in form.errors[error]:
                messages.error(request, err)
    form = todolist.forms.TodoListForm(request.user)
    return render(request=request, template_name="todolist/index.html", context={"todolist": todos, "form": form})


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
        todo = todolist.models.TodoList.objects.get(id=request.POST["todo_id"])
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
def update_comment(request):
    try:
        comment = todolist.models.Comments.objects.get(id=request.POST["comment_id"])
        comment_text = request.POST["comment_text"]
        if len(comment_text) < 1:
            messages.error(request, "Comment is required.")
        if comment.author != request.user:
            messages.error(request, "You are not authorized to update this comment.")
            return redirect("index")
        comment.comment = comment_text
        comment.save(update_fields=["comment"])
        messages.info(request, "Comment updated successfully.")
    except KeyError:
        messages.error(request, "Id and comment is required.")
    except todolist.models.Comments.DoesNotExist:
        messages.error(request, "Comment does not exist.")
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