from django import forms
from django.forms import fields
from .models import Department, Note, QuestionPaper, Book, VideoTutorial, WebTutorial

class DepartmentSemesterForm(forms.Form):
    dept_choices = Department.all_department()
    dept_choices = [ (ele.get('name'), ele.get('name')) for ele in dept_choices]
    sem_choices = [1,2,3,4,5,6,7,8]
    sem_choices = [ (ele, ele) for ele in sem_choices]
    dept_name = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-select','id':'dept_name', 'placeholder':'Choose Department'}), choices=dept_choices)
    semester = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-select','id':'semester', 'placeholder':'Choose Semester'}), choices=sem_choices)

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['topic', 'file']

class QuestionPaperForm(forms.ModelForm):
    class Meta:
        model = QuestionPaper
        fields = ['subject', 'year', 'file']

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['subject', 'name', 'author', 'view_link']

class VideoTutorialForm(forms.ModelForm):
    class Meta:
        model = VideoTutorial
        fields = ['subject', 'name', 'view_link']

class WebTutorialForm(forms.ModelForm):
    class Meta:
        model = WebTutorial
        fields = ['subject', 'name', 'view_link']