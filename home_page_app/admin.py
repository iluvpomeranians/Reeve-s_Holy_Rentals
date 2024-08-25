from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'firstName', 'lastName', 'driverLicense', 'address', 'city', 'state', 'membership', 'dateofbirth', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'membership')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('firstName', 'lastName', 'driverLicense', 'address', 'city', 'state', 'dateofbirth')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'firstName', 'lastName', 'driverLicense', 'address', 'city', 'state', 'dateofbirth', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )
    search_fields = ('email', 'firstName', 'lastName', 'driverLicense', 'address', 'city', 'state')
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, CustomUserAdmin)
