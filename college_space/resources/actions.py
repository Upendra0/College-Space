""" Admin action for resources"""

from django.contrib import admin


@admin.action(description="Verify selected items")
def make_resource_verified(modeladmin, request, queryset):
    ''' Set all resources as verified. '''
    queryset.update(is_approved=True)