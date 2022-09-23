from django.shortcuts import render, redirect
from .forms import MyUserCreationForm
from django.contrib.auth import login
from django.contrib import messages
import django.contrib.auth
import django.http
import django.urls

_POST = "POST"
_GET = "GET"


def register(request):
    if request.method == _POST:
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("login")
        for error in form.errors:
            for err in form.errors[error]:
                messages.error(request, err)
    form = MyUserCreationForm()
    return render(request=request, template_name="auth/register.html", context={"form": form})

def logout(request):
    django.contrib.auth.logout(request)
    return django.http.response.HttpResponseRedirect(django.urls.reverse('index'))
