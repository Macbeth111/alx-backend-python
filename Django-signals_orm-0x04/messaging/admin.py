from django.contrib import admin  # type: ignore
from .models import Message, Notification

admin.site.register(Message)
admin.site.register(Notification)
