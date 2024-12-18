from django.contrib import admin
from .models import TLSA_User
from django.contrib.auth.admin import UserAdmin

@admin.register(TLSA_User)
class CustomUserAdmin(UserAdmin):
    readonly_fields = ("user_id",)

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = ("user_id","role") + self.list_display

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'phone_number', 'role', 'profile_picture', 'department')}),
        #('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )