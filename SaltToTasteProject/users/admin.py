from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['avatar', 'name', 'nickname', 'email']
    list_display_links = ['avatar', 'name', 'nickname', 'email']

    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (
            'Пользовательская информация',
            {
                'fields': (
                    'avatar',
                    'name',
                    'nickname',
                    # 'email',
                )
            }
        )
    )
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Пользовательская информация',
            {
                'fields': (
                    'avatar',
                    'name',
                    'nickname',
                    # 'email',
                )
            }
        )
    )


admin.site.register(CustomUser, CustomUserAdmin)
