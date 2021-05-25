from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'is_staff']
    search_fields = ['email', 'username']
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email','profile_image')}),
        (('Permissions'), {'fields': ('is_active','is_staff', 'is_superuser', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')})
    )
    readonly_fields = ["date_joined", "last_login"]
    filter_horizontal = []
    list_filter = []


admin.site.register(CustomUser, CustomUserAdmin)
