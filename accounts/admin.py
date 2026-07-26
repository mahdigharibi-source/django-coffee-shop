from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from accounts.models import CustomUser, Profile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = CustomUser
    ordering = ['email']
    list_display = ['email', 'is_superuser', 'is_verified', 'is_active']
    list_display_links = ('email',)
    list_filter = ['is_verified', 'is_active']
    list_editable = ['is_verified']
    list_per_page = 6

    add_fieldsets = (
        ('Authentication', {
            'fields': (
                'email', 'password1', 'password2'
            )
        }),
        (None, {
            'fields': (
                'is_active', 'is_staff', 'is_verified', 'is_superuser', 'user_type'
            )
        })
    )

    fieldsets = (
        ('Authentication', {
            'fields': (
                'email', 'password'
            )
        }),

        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_verified', 'is_superuser'
            )
        }),

        ('group permissions', {
            'fields': (
                'groups', 'user_permissions', 'user_type'
            )
        }),

        ('Important data', {
            'fields': (
                'last_login',
            )
        }),
    )



admin.site.register(Profile)
