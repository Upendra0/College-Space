from django import forms
from django.forms import fields, widgets
from .models import Department, Note, QuestionPaper, Book, VideoTutorial, WebTutorial

class DepartmentSemesterForm(forms.Form):
    dept_choices = Department.all_department()
    dept_choices = [ (ele.get('name'), ele.get('name')) for ele in dept_choices]
    sem_choices = [1,2,3,4,5,6,7,8]
    sem_choices = [ (ele, ele) for ele in sem_choices]
    dept_name = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-select','id':'dept_name', 'placeholder':'Choose Department'}), choices=dept_choices, required=False)
    semester = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-select','id':'semester', 'placeholder':'Choose Semester'}), choices=sem_choices, required=False)

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['topic', 'file']
        widgets = {
            'topic': forms.Select(attrs={'class':'form-select', 'id':'topic', 'placeholder':'select topic name'}),
            'file': forms.FileInput(attrs={'class':'form-control', 'id':'file', 'type':'file'})
        }

class QuestionPaperForm(forms.ModelForm):
    class Meta:
        model = QuestionPaper
        fields = ['subject', 'year', 'file']
        widgets = {
            'subject': forms.Select(attrs={'class':'form-select', 'id':'subject', 'placeholder':'select subject name'}),
            'year': forms.TextInput(attrs={'class':'form-control', 'id':'year', 'placeholder':'Year'}),
            'file': forms.FileInput(attrs={'class':'form-control', 'id':'file', 'type':'file'})
        }

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['subject', 'name', 'author', 'view_link']
        widgets = {
            'subject': forms.Select(attrs={'class':'form-select', 'id':'subject', 'placeholder':'select subject name'}),
            'name': forms.TextInput(attrs={'class':'form-control', 'id':'name', 'placeholder':"Book's Name"}),
            'author': forms.TextInput(attrs={'class':'form-control', 'id':'author', 'placeholder':"Author's Name"}),
            'view_link': forms.TextInput(attrs={'class':'form-control', 'id':'view_link', 'placeholder':"Book's Link"}),
        }

class VideoTutorialForm(forms.ModelForm):
    class Meta:
        model = VideoTutorial
        fields = ['subject', 'name', 'view_link']
        widgets = {
            'subject': forms.Select(attrs={'class':'form-select', 'id':'subject', 'placeholder':'select subject name'}),
            'name': forms.TextInput(attrs={'class':'form-control', 'id':'name', 'placeholder':"Tutorials's Name"}),
            'view_link': forms.TextInput(attrs={'class':'form-control', 'id':'view_link', 'placeholder':"Tutorials's Link"}),
        }

class WebTutorialForm(forms.ModelForm):
    class Meta:
        model = WebTutorial
        fields = ['subject', 'name', 'view_link']
        widgets = {
            'subject': forms.Select(attrs={'class':'form-select', 'id':'subject', 'placeholder':'select subject name'}),
            'name': forms.TextInput(attrs={'class':'form-control', 'id':'name', 'placeholder':"Tutorials's Name"}),
            'view_link': forms.TextInput(attrs={'class':'form-control', 'id':'view_link', 'placeholder':"Tutorials's Link"}),
        }