from django.urls import path
import todolist.views

urlpatterns = [
    path('remove-todo/', todolist.views.remove_todo, name="remove_todo"),
    path('add-comment/', todolist.views.add_comment, name="add_comment"),
    path('update-comment/', todolist.views.update_comment, name="update_comment"),
    path('remove-comment/', todolist.views.remove_comment, name="remove_comment"), ]
