from django.contrib import admin
from .models import Subject, Resource, Syllabus, Note

class SubjectAdmin(admin.ModelAdmin):
    list_display= ['name', 'sub_code', 'department', 'semester', 'credit']
    list_filter= ['department', 'semester', 'credit']

class ResourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'resource_type', 'get_semester', 'get_department', 'link']
    list_filter= ['subject']

class SyllabusAdmin(admin.ModelAdmin):
    list_display = ['department', 'semester', 'download_link']
    list_filter= ['department', 'semester']

class NoteAdmin(admin.ModelAdmin):
    list_display = ['subject', 'topic', 'uploaded_by', 'file']
    list_filter = ['uploaded_by']

# Register your models here.
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Syllabus, SyllabusAdmin)
admin.site.register(Note, NoteAdmin)

