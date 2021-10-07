from django.contrib import admin
from django.contrib.admin.filters import ListFilter
from . import models

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

class SubjectAdmin(admin.ModelAdmin):
    list_display = [ 'code', 'name', 'credit']
    list_filter = ['credit']
    ordering = ['name']
    search_fields = ['code', 'name']

class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject']
    list_filter = ['subject']
    ordering = ['name']
    search_fields = ['name', 'subject__name']

class TaughtAdmin(admin.ModelAdmin):
    list_display = ['subject', 'department', 'semester']
    list_filter = ['department', 'semester']
    ordering = ['department']
    search_fields = ['subject__name', 'department__name']

class SyllabusAdmin(admin.ModelAdmin):
    list_display = ['department', 'semester', 'view_link']
    list_filter = ['department', 'semester']
    ordering= ['department']
    search_fields = ['department']

class NoteAdmin(admin.ModelAdmin):
    list_display = ['topic', 'file', 'contributor', 'is_approved']
    list_filter = ['is_approved', 'contributor']
    search_fields = ['topic__name', 'contributor__email']

class BookAdmin(admin.ModelAdmin):
    list_display = ['subject', 'name', 'view_link', 'contributor', 'is_approved']
    list_filter = ['is_approved', 'contributor']
    ordering = ['name']
    search_fields = ['name', 'subject__name', 'contributor__email']

class WebTutorialAdmin(admin.ModelAdmin):
    list_display = ['subject', 'name', 'view_link', 'contributor', 'is_approved']
    list_filter = ['is_approved', 'contributor']
    ordering = ['name']
    search_fields = ['name', 'subject__name','contributor__email']

class VideoAdmin(admin.ModelAdmin):
    list_display = ['subject', 'name', 'view_link', 'contributor', 'is_approved']
    list_filter = ['is_approved', 'contributor']
    ordering = ['name']
    search_fields = ['name', 'subject__name', 'contributor__email']

class QuestionPaperAdmin(admin.ModelAdmin):
    list_display = ['subject', 'year', 'file', 'contributor', 'is_approved']
    list_filter = ['is_approved', 'year', 'contributor']
    ordering = ['subject']
    search_fields = ['subject__name', 'year', 'contributor__email']


admin.site.register(models.Department, DepartmentAdmin)
admin.site.register(models.Subject, SubjectAdmin)
admin.site.register(models.Topic, TopicAdmin)
admin.site.register(models.Taught, TaughtAdmin)
admin.site.register(models.Syllabus, SyllabusAdmin)
admin.site.register(models.Note, NoteAdmin)
admin.site.register(models.Book, BookAdmin)
admin.site.register(models.WebTutorial, WebTutorialAdmin)
admin.site.register(models.Video, VideoAdmin)
admin.site.register(models.QuestionPaper, QuestionPaperAdmin)