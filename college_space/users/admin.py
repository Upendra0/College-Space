''' Admin site settings for User and Group Class.'''

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin
from django.contrib.auth.models import Group

from .models import User
from .forms import GroupAdminForm


class UserAdmin(BaseUserAdmin):

    '''Admin class for User Model'''

    # Fields to display for each user.
    list_display = ['email', 'first_name', 'last_name', 'department', 'semester', 'profile_pic']

    # List of filters.
    list_filter = ['department', 'is_staff', 'is_superuser']
    
    # Fieldsets for viewing a user.
    fieldsets = [
        (None, {'fields': ('password',)}),
        ('Personal Info', {'fields': (
            'first_name', 'last_name', 'department', 'semester', 'profile_pic')}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')})
    ]

    # Fieldsets for creating a new user.
    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2', 'first_name', 'last_name',
         'department', 'semester', 'profile_pic', 'is_staff', 'is_superuser')}),
    )

    # Fields used in searching a user.
    search_fields = ('email', 'first_name', 'last_name')

    # User's are sorted by their joining date.
    ordering = ('date_joined',)

class GroupAdmin(admin.ModelAdmin):
    
    ''' Admin class for Group Model'''

    # Use our custom form.
    form = GroupAdminForm

    # Filter permissions horizontal as well.
    filter_horizontal = ['permissions']


# UnRegister old group and Register the customised group in admin.
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)

# Register the user model
admin.site.register(User, UserAdmin)
