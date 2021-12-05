""" Admin Page settings for resources."""

from django.contrib import admin

from . import models
from .actions import make_resource_verified

class DepartmentAdmin(admin.ModelAdmin):

    ''' Admin class for Department model.'''

    list_display = ['name']
    search_fields = ['name']

class SubjectAdmin(admin.ModelAdmin):

    ''' Admin class for Subject model.'''

    list_display = [ 'code', 'name', 'credit']
    list_filter = ['credit']
    ordering = ['name']
    search_fields = ['code', 'name']

class TopicAdmin(admin.ModelAdmin):

    ''' Admin class for Topic model.'''

    list_display = ['name', 'subject']
    list_filter = ['subject']
    ordering = ['name']
    search_fields = ['name', 'subject__name']

class TaughtAdmin(admin.ModelAdmin):

    ''' Admin class for Taught model.'''

    list_display = ['subject', 'department', 'semester']
    list_filter = ['department', 'semester']
    ordering = ['department']
    search_fields = ['subject__name', 'department__name']

class SyllabusAdmin(admin.ModelAdmin):

    ''' Admin class for Syllabus model.'''

    list_display = ['department', 'semester', 'view_link']
    list_filter = ['department', 'semester']
    ordering= ['department']
    search_fields = ['department']

class NoteAdmin(admin.ModelAdmin):

    ''' Admin class for Note model.'''

    list_display = ['topic', 'file', 'contributor', 'is_approved']
    list_filter = ['is_approved', 'contributor']
    search_fields = ['topic__name', 'contributor__email']
    actions =[make_resource_verified]

class BookAdmin(admin.ModelAdmin):

    ''' Admin class for Book model.'''

    list_display = ['subject', 'name', 'view_link', 'contributor', 'is_approved']
    list_filter = ['is_approved', 'contributor']
    ordering = ['name']
    search_fields = ['name', 'subject__name', 'contributor__email']
    actions = [make_resource_verified]

class WebTutorialAdmin(admin.ModelAdmin):

    ''' Admin class for WebTutorial model.'''

    list_display = ['subject', 'name', 'view_link', 'contributor', 'is_approved']
    list_filter = ['is_approved', 'contributor']
    ordering = ['name']
    search_fields = ['name', 'subject__name','contributor__email']
    actions = [make_resource_verified]

class VideoTutorialAdmin(admin.ModelAdmin):

    ''' Admin class for VideoTutorial model.'''

    list_display = ['subject', 'name', 'view_link', 'contributor', 'is_approved']
    list_filter = ['is_approved', 'contributor']
    ordering = ['name']
    search_fields = ['name', 'subject__name', 'contributor__email']
    actions = [make_resource_verified]

class QuestionPaperAdmin(admin.ModelAdmin):

    ''' Admin class for QuestionPaper model.'''

    list_display = ['subject', 'year', 'file', 'contributor', 'is_approved']
    list_filter = ['is_approved', 'year', 'contributor']
    ordering = ['subject']
    search_fields = ['subject__name', 'year', 'contributor__email']
    actions = [make_resource_verified]


admin.site.register(models.Department, DepartmentAdmin)
admin.site.register(models.Subject, SubjectAdmin)
admin.site.register(models.Topic, TopicAdmin)
admin.site.register(models.Taught, TaughtAdmin)
admin.site.register(models.Syllabus, SyllabusAdmin)
admin.site.register(models.Note, NoteAdmin)
admin.site.register(models.Book, BookAdmin)
admin.site.register(models.WebTutorial, WebTutorialAdmin)
admin.site.register(models.VideoTutorial, VideoTutorialAdmin)
admin.site.register(models.QuestionPaper, QuestionPaperAdmin)