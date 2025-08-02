from django.contrib import admin  # type: ignore
from .models import Message, Notification, MessageHistory

admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(MessageHistory)
