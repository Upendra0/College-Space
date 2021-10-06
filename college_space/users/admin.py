from .models import User
from django.contrib import admin
from .forms import UserChangeForm, UserCreationForm, GroupAdminForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as origGroupAdmin
from django.contrib.auth.models import Group

# Register your models here.
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ['email', 'first_name', 'last_name', 'department', 'semester', 'profile_pic']
    list_filter = ['semester', 'department', 'is_staff', 'is_superuser']

    fieldsets = [
        (None, {'fields':('email', 'password')}),
        ('Personal Info', {'fields':('first_name', 'last_name', 'department', 'semester', 'profile_pic')}),
        ('Permissions', {'fields':('is_staff', 'is_superuser', 'groups', 'user_permissions')})
    ]

    add_fieldsets = (
        (None, {'fields':('email', 'password1', 'password2', 'first_name', 'last_name','department', 'semester', 'profile_pic', 'is_staff', 'is_superuser')}),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

class GroupAdmin(origGroupAdmin):
    """
    Customized GroupAdmin class that uses the customized form to allow
    management of users within a group.
    """
    form = GroupAdminForm

# Register User model to admin site.
admin.site.register(User, UserAdmin)


# Register the modified GroupAdmin with the admin site
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)