from django.contrib import admin
from .models import Contributor

# Register your models here.
class ContributorAdmin(admin.ModelAdmin):
    list_display = ['user', 'college_id']

admin.site.register(Contributor, ContributorAdmin)