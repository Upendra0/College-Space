from django.contrib import admin
from django.contrib.admin.filters import ListFilter
from . import models

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']

class SubjectAdmin(admin.ModelAdmin):
    list_display = [ 'code', 'name', 'credit']
    list_filter = ['credit']

class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject']
    list_filter = ['subject']

class TaughtAdmin(admin.ModelAdmin):
    list_display = ['subject', 'department', 'semester']
    list_filter = ['department', 'semester']

class SyllabusAdmin(admin.ModelAdmin):
    list_display = ['department', 'semester', 'view_link']
    list_filter = ['department', 'semester']

class NoteAdmin(admin.ModelAdmin):
    list_display = ['topic', 'file', 'contributor', 'is_approved']
    list_filter = ['is_approved', 'contributor']

class BookAdmin(admin.ModelAdmin):
    list_display = ['subject', 'name', 'view_link', 'contributor', 'is_approved']
    list_filter = ['is_approved', 'contributor']

class WebTutorialAdmin(admin.ModelAdmin):
    list_display = ['subject', 'name', 'view_link', 'contributor', 'is_approved']
    list_filter = ['is_approved', 'contributor']

class VideoAdmin(admin.ModelAdmin):
    list_display = ['subject', 'name', 'view_link', 'contributor', 'is_approved']
    list_filter = ['is_approved', 'contributor']

class QuestionPaperAdmin(admin.ModelAdmin):
    list_display = ['subject', 'year', 'file', 'contributor', 'is_approved']
    list_filter = ['is_approved', 'year', 'contributor']


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