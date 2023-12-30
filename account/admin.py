from django.contrib import admin
from .models import User

class UserModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "name",
        "username",
        "date_created",
        "date_updated",
        "is_active",
        "is_admin",
    )
admin.site.register(User, UserModelAdmin)
