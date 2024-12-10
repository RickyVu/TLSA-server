from django.contrib import admin
from .models import TLSA_User
from django.contrib.auth.admin import UserAdmin

@admin.register(TLSA_User)
class CustomUserAdmin(UserAdmin):
    readonly_fields = ("id",)

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = ("id","role") + self.list_display

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'role')}),
        #('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )