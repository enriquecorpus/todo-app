from django.shortcuts import render, redirect
import django.contrib.auth.decorators


@django.contrib.auth.decorators.login_required
def index(request):
    return render(request=request, template_name="todolist/index.html", context={"form": ""})

