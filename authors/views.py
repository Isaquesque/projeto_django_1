from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.http import HttpResponse, Http404

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            return HttpResponse("ok", status=200)
    else: 
        form = RegisterForm(request.session["POST"])

    return render(request, "authors/register.html", context={"form":form})

def register_create(request):
    if request.method == "GET":
        raise Http404
    
    POST = request.POST
    request.session["POST"] = POST
    return redirect("register")