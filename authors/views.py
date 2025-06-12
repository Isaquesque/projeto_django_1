from django.shortcuts import render
from .forms import RegisterForm
from django.http import HttpResponse

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            return HttpResponse("ok", status=200)
    else: 
        form = RegisterForm()

    return render(request, "authors/register.html", context={"form":form})