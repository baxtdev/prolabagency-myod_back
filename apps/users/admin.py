from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _

from .models import User,ResetPasword

# Register your models here.
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        fields = ('email','passowrd','passowrd1')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'email', 
        'get_full_name', 
        'phone', 
        'last_activity'
        )
    readonly_fields = (
        'my_purchases_count',
        'my_reviews_count',
        'my_products_count',
        'my_orders_count'
        )
    fieldsets = (
        (None, {'fields': (
            'email',
            'phone',
            'password',
        )}),
        (_('Personal info'), {'fields': (
            'image',
            'first_name',
            'last_name',
            'middle_name'
        )}),
        (_('Permissions'), {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
        (_('Important dates'), {'fields': (
            'date_joined',
            'last_login',
        )}),
        (_('info'), {'fields': (
            'my_purchases_count',
            'my_reviews_count',
            'my_products_count',
            'my_orders_count'
        )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'phone',
                'password1',
                'password2',
            ),
        }),
    )

    search_fields = (
        'email', 
        'first_name', 
        'last_name'
        )
    
    ordering = ('email',)


@admin.register(ResetPasword)
class ResetPasswordAdmin(admin.ModelAdmin):
    pass