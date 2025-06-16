from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def register(request):
    if request.method == "POST":
        data = request.POST
        bound_form = RegisterForm(data)

        if bound_form.is_valid():
            cleaned_data = bound_form.cleaned_data
            del cleaned_data["password2"]
            user = User.objects.create_user(**cleaned_data)
            messages.add_message(request, messages.SUCCESS, f"Usuário {user.username} cadastrado com sucesso")
        else:
            messages.add_message(request, messages.ERROR, "O formulário possui erros. Corrija-os")
            return render(request, "authors/register.html", context={"form":bound_form})

    form = RegisterForm()
    return render(request, "authors/register.html", context={"form":form})