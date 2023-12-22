from django.contrib import admin

# Register your models here.
from htmx_todo_app.models import TodoItem
admin.site.register(TodoItem)
