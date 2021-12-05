""" Form for Resource app."""

from django import forms

from .models import Department, Note, QuestionPaper, Book, VideoTutorial, WebTutorial


class DepartmentSemesterForm(forms.Form):

    ''' Form to get department and semester.'''

    dept_choices = Department.all_department()
    dept_choices = [ (ele.get('name'), ele.get('name')) for ele in dept_choices]
    sem_choices = [1,2,3,4,5,6,7,8]
    sem_choices = [ (ele, ele) for ele in sem_choices]
    dept_name = forms.ChoiceField(
        widget=forms.Select(attrs={'class':'form-select','id':'dept_name', 'placeholder':'Choose Department'}),
        choices=dept_choices, 
        required=False
        )
    semester = forms.ChoiceField(
        widget=forms.Select(attrs={'class':'form-select','id':'semester', 'placeholder':'Choose Semester'}), 
        choices=sem_choices, 
        required=False
        )

class NoteForm(forms.ModelForm):

    '''Django model form to create Note.
    
    Fields are:
    topic - Topic of the Note.
    file - Note's pdf file.
    '''
    class Meta:
        model = Note
        fields = ['topic', 'file']
        widgets = {
            'topic': forms.Select(attrs={'class':'form-select', 'id':'topic', 'placeholder':'select topic name'}),
            'file': forms.FileInput(attrs={'class':'form-control', 'id':'file', 'type':'file'})
        }

class QuestionPaperForm(forms.ModelForm):

    '''Django model form to create QuestionPaper.
    
    Fields are:
    subject - QuestionPaper's subject
    year -QuestionPaper's year
    file - QuestionPaper's pdf file.
    '''

    class Meta:
        model = QuestionPaper
        fields = ['subject', 'year', 'file']
        widgets = {
            'subject': forms.Select(attrs={'class':'form-select', 'id':'subject', 'placeholder':'select subject name'}),
            'year': forms.TextInput(attrs={'class':'form-control', 'id':'year', 'placeholder':'Year'}),
            'file': forms.FileInput(attrs={'class':'form-control', 'id':'file', 'type':'file'})
        }

class BookForm(forms.ModelForm):

    '''Django model form to create Book.
    
    Fields are:
    subject - Book's subject
    name - Book's name
    author - Book's author
    view_link - Book's download link
    '''

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

    '''Django model form to create VideoTutorial.
    
    Fields are:
    subject - QuestionPaper's subject
    name - Tutorials's name
    view_link - Tutorials's link
    '''

    class Meta:
        model = VideoTutorial
        fields = ['subject', 'name', 'view_link']
        widgets = {
            'subject': forms.Select(attrs={'class':'form-select', 'id':'subject', 'placeholder':'select subject name'}),
            'name': forms.TextInput(attrs={'class':'form-control', 'id':'name', 'placeholder':"Tutorials's Name"}),
            'view_link': forms.TextInput(attrs={'class':'form-control', 'id':'view_link', 'placeholder':"Tutorials's Link"}),
        }

class WebTutorialForm(forms.ModelForm):

    '''Django model form to create WebTutorial.
    
    Fields are:
    subject - QuestionPaper's subject
    name - Tutorials's name
    view_link - Tutorials's link
    '''
    class Meta:
        model = WebTutorial
        fields = ['subject', 'name', 'view_link']
        widgets = {
            'subject': forms.Select(attrs={'class':'form-select', 'id':'subject', 'placeholder':'select subject name'}),
            'name': forms.TextInput(attrs={'class':'form-control', 'id':'name', 'placeholder':"Tutorials's Name"}),
            'view_link': forms.TextInput(attrs={'class':'form-control', 'id':'view_link', 'placeholder':"Tutorials's Link"}),
        }