from django.contrib import admin
from .models import Subject, Resource, Syllabus

class SubjectAdmin(admin.ModelAdmin):
    list_display= ['name', 'sub_code', 'department', 'semester', 'credit']
    list_filter= ['department', 'semester', 'credit']

class ResourceAdmin(admin.ModelAdmin):
    list_display = ['subject', 'resource_type', 'get_semester', 'get_department','author', 'link']
    list_filter= ['author']

class SyllabusAdmin(admin.ModelAdmin):
    list_display = ['department', 'semester', 'download_link']
    list_filter= ['department', 'semester']

# Register your models here.
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Syllabus, SyllabusAdmin)
