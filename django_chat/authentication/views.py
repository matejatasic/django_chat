from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin

from .forms import UserRegisterForm


class LoginView(UserPassesTestMixin, TemplateView):
    template_name = "login.html"

    def test_func(self) -> bool:
        return self.request.user.is_anonymous

    def post(self, request: HttpRequest) -> HttpResponse:
        form: AuthenticationForm = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user: User = self._authenticate_user(form)

            if user is not None:
                login(request, user)

                return redirect("/public_chat")

        return render(request, "login.html", context={"login_form": form})

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "login.html", context={"login_form": AuthenticationForm})

    def _authenticate_user(self, form: AuthenticationForm) -> User:
        username: str = form.cleaned_data.get("username")
        password: str = form.cleaned_data.get("password")
        user: User = authenticate(username=username, password=password)

        return user

class RegisterView(UserPassesTestMixin, TemplateView):
    template_name = "register.html"

    def test_func(self) -> bool:
        return self.request.user.is_anonymous

    def post(self, request: HttpRequest) -> HttpResponse:
        form: UserRegisterForm = UserRegisterForm(request.POST, request.FILES)

        if form.is_valid():
            user: User = form.save()
            login(request, user)

            return redirect("/public_chat")

        return render(request, "register.html", context={"register_form": form})

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "register.html", context={"register_form": UserRegisterForm})

@login_required(login_url="/login")
def logout_user(request: HttpRequest) -> HttpResponse:
    logout(request)

    return redirect("/")