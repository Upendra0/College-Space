from .models import User
from django.contrib import admin
from django.contrib.auth.models import Group
from . import forms 
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
class UserAdmin(BaseUserAdmin):
    form = forms.UserChangeForm
    add_form = forms.UserCreationForm

    list_display = ['email', 'first_name', 'last_name', 'department', 'semester']
    list_filter = ['email', 'semester', 'first_name', 'is_admin']

    fieldsets = [
        (None, {'fields':('email', 'password')}),
        ('Personal Info', {'fields':('first_name', 'last_name', 'department', 'semester')}),
        ('Permissions', {'fields':('is_admin',)})
    ]

    add_fieldsets = (
        (None, {'fields':('email', 'password1', 'password2', 'first_name', 'last_name','department', 'semester')}),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)