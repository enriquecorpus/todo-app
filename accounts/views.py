from django.shortcuts import render, redirect
from .forms import MyUserCreationForm
from django.contrib.auth import login
from django.contrib import messages
import django.contrib.auth
import django.urls

_POST = "POST"
_GET = "GET"


def register(request):
    form = MyUserCreationForm()
    if request.method == _POST:
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
        for error in form.errors:
            for err in form.errors[error]:
                messages.error(request, err)
    return render(request=request, template_name="auth/register.html", context={"form": form})


def logout(request):
    django.contrib.auth.logout(request)
    return redirect(django.urls.reverse('index'))
