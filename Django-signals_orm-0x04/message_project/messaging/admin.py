from django.contrib import admin
from .models import Message, Notification
from django.urls import path, include

# Register your models here.

urlpatterns = [path("admin/", admin.site.urls)]

admin.site.register(Message)
admin.site.register(Notification)
