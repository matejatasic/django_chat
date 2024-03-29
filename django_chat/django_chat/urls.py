"""django_chat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

from django.conf.urls.static import static
from django.conf import settings

from public_chat.api import PublicChatModelViewSet
from private_chat.api import PrivateChatModelViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"public_chat", PublicChatModelViewSet, basename="public-chat-api")
router.register(r"private-chat", PrivateChatModelViewSet, basename="private-chat-api")

app_name = "django_chat"

urlpatterns = [
    path("api/", include(router.urls)),
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="home.html"), name="homepage"),
    path("public_chat", include("public_chat.urls")),
    path("private_chat", include("private_chat.urls")),
    path("", include("authentication.urls")),
]

urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
