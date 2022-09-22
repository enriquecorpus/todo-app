from django.shortcuts import render, redirect
from .forms import MyUserCreationForm
from django.contrib.auth import login
from django.contrib import messages


def register(request):
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("main:homepage")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = MyUserCreationForm()
    return render(request=request, template_name="auth/register.html", context={"form": form})
