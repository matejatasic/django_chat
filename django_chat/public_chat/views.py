from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required


@login_required(login_url="/login")
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "public_chat.html")