from django.urls import reverse
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin


class PrivateChatView(LoginRequiredMixin, TemplateView):
    template_name = "private_chat.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        users = User.objects.all().exclude(pk=request.user.id)

        return render(request, "private_chat.html", context={"users": users})

    def get_login_url(self) -> str:
        return reverse("login")