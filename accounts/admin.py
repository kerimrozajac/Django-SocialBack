# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "email",
        "username",
        #"name",
        "is_staff",
    ]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("public_id",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("public_id",)}),)

    def get_readonly_fields(self, request, obj=None):
        # Make 'public_id' read-only
        readonly_fields = super().get_readonly_fields(request, obj)
        return readonly_fields + ('public_id',)


admin.site.register(CustomUser, CustomUserAdmin)