from django.contrib import admin

@admin.action(description="Verify selected items")
def make_resource_verified(modeladmin, request, queryset):
    queryset.update(is_approved=True)