from django.contrib import admin
from .models import PrivateDialog, PrivateMessage

admin.site.register(PrivateDialog)
admin.site.register(PrivateMessage)
