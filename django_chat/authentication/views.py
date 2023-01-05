from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm


class LoginView(TemplateView):
    template_name = "login.html"

    def post(self, request: HttpRequest) -> HttpResponse:
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = self._authenticate_user(form)

            if user is not None:
                login(request, user)

                return redirect("/public_chat")

        return render(request, "login.html", context={"login_form": form})

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "login.html", context={"login_form": AuthenticationForm})

    def _authenticate_user(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)

        return user

class RegisterView(TemplateView):
    template_name = "register.html"

    def post(self, request: HttpRequest) -> HttpResponse:
        form = UserRegisterForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect("/public_chat")

        return render(request, "register.html", context={"register_form": form})

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "register.html", context={"register_form": UserRegisterForm})

@login_required
def logout_user(request):
    logout(request)

    return redirect("/")