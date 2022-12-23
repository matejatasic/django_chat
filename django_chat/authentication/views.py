from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Create your views here.
def login(request: HttpRequest) -> HttpResponse:
    return render(request, "login.html")

def register(request: HttpRequest) -> HttpResponse:
    return render(request, "register.html")