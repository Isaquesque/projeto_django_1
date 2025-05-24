from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(
        request, 
        "home.html", 
        content_type="text/html", 
        context={"nome":"isaque"}
    )


