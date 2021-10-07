from .models import User
from django.contrib import admin
from .forms import GroupAdminForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin
from django.contrib.auth.models import Group

# Register your models here.
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'profile_pic', 'department', 'semester']
    list_filter = ['department', 'is_staff', 'is_superuser']

    fieldsets = [
        (None, {'fields':('password',)}),
        ('Personal Info', {'fields':('first_name', 'last_name','department', 'semester', 'profile_pic')}),
        ('Permissions', {'fields':('is_staff', 'is_superuser', 'groups', 'user_permissions')})
    ]

    add_fieldsets = (
        (None, {'fields':('email', 'password1', 'password2', 'first_name', 'last_name', 'department', 'semester', 'profile_pic', 'is_staff', 'is_superuser')}),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('date_joined',)
    filter_horizontal = ()

#New Group admin.
class GroupAdmin(admin.ModelAdmin):
    # Use our custom form.
    form = GroupAdminForm
    # Filter permissions horizontal as well.
    filter_horizontal = ['permissions']

# UnRegister old group and Register the customised group in admin.
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)

# Register the user model
admin.site.register(User, UserAdmin)