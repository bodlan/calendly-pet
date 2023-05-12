from django.contrib import admin
from .models import User, Event

# Register your models here.

admin.site.register(Event)


class UserAdmin(admin.ModelAdmin):
    fieldsets = [("Basic info", {"fields": ["username", "password"]}), ("Date related", {"fields": ["timezone"]})]


admin.site.register(User, UserAdmin)
