""" Resource's models"""

from typing import List
from django.db import models
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class Department(models.Model):

    ''' Department model, store each department information '''

    name = models.CharField(max_length=50, primary_key=True)
    class Meta:
        db_table = 'department'

    @classmethod
    def all_department(cls) ->List:
        ''' Return list of all department's name.'''

        return cls.objects.all().values('name')

    def __str__(self) -> str:
        ''' Str representation of department.'''

        return self.name


class Subject(models.Model):

    '''Subject model, store information of each subject.
    
    Fields are:
    code - subject's code
    name - subject's name
    credit - subject's credit
    '''

    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=50)
    credit = models.FloatField(validators=[MinValueValidator(0)])

    class Meta:
        db_table = 'subject'

    @classmethod
    def get_name(cls, sub_code: str) -> str:
        ''' Return the name of subject of given sub_code.'''

        try:
            return cls.objects.get(code=sub_code).name
        except Subject.DoesNotExist:
            return None

    def __str__(self) -> str:
        '''Str representaion of subject.'''

        return self.name

class Taught(models.Model):

    ''' Store the information of subject taught in each department and semester.'''

    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE, db_column='sub_code')
    department = models.ForeignKey(to=Department, on_delete=models.CASCADE, db_column='dept_name')
    semester = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])

    class Meta:
        db_table = 'taught'

        #A subject can not be taught more than once in a department.
        unique_together = [['subject', 'department']]

    @classmethod
    def get_subjects(cls, dept_name, semester):
        '''Returns the set of subjects taught in particular department in particular semester.'''

        return cls.objects.filter(department__name=dept_name, semester=semester).values('subject__code', 'subject__name', 'subject__credit')
        

    def __str__(self) -> str:
        '''Str representaion of taught.'''

        return self.subject.name + self.department.name

class Book(models.Model):

    ''' Store the information of each book.
    
    fields:\n
    suject - book's subject, foreign key to Subject.\n
    name - charfield storing book's name.\n
    author - charfield storing book's author.\n
    view_link - charfield storing download link of book.\n
    contributor - book's contributor, foreign key to user.\n
    is_approved - bool representing wheather book is approved or not.\n
    '''

    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE, db_column='sub_code')
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    view_link = models.CharField(max_length=500, unique=True)
    contributor = models.ForeignKey(to='users.User', on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    class Meta:
        db_table = 'book'

    @classmethod
    def total_not_verified(cls, user) ->int:
        '''Return total Books contributed by user which is not approved.'''

        return len(cls.objects.filter(contributor=user, is_approved=False))

    @classmethod
    def get_books(cls, sub_code: str) ->List:
        ''' Return set of books of a subject'''
        return cls.objects.filter(subject__code=sub_code, is_approved=True).values('name', 'author', 'view_link')

    def __str__(self) -> str:
        '''Str representaion of book.'''

        return self.name


class WebTutorial(models.Model):

    ''' Store the information of each WebTutorial.
    
    fields:\n
    suject - foreign key to Subject representing tutorial's subject.\n
    name - charfield storing tutorials's name.\n
    view_link - charfield storing link of tutorial.\n
    contributor - tutorial's contributor, foreign key to user.\n
    is_approved - bool representing wheather tutorial is approved or not.\n
    '''

    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE, db_column='sub_code')
    name = models.CharField(max_length=50)
    view_link = models.CharField(max_length=500, unique=True)
    contributor = models.ForeignKey(to='users.User', on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    class Meta:
        db_table = 'web_tutorial'

    @classmethod
    def get_web_tutorials(cls, sub_code: str) ->List:
        ''' Returns all web tutorial whoose subject's code is sub_code.'''

        return cls.objects.filter(subject__code=sub_code, is_approved=True).values('name','view_link')

    @classmethod
    def total_not_verified(cls, user) -> int:
        '''Return total Web tutorials contributed by user which is not approved.'''

        return len(cls.objects.filter(contributor=user, is_approved=False))

    def __str__(self) -> str:
        return self.name

class VideoTutorial(models.Model):

    ''' Store the information of each VideoTutorial.
    
    fields:\n
    suject - foreign key to Subject representing tutorial's subject.\n
    name - charfield storing tutorials's name.\n
    view_link - charfield storing link of tutorial.\n
    contributor - tutorial's contributor, foreign key to user.\n
    is_approved - bool representing wheather tutorial is approved or not.\n
    '''

    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE, db_column='sub_code')
    name = models.CharField(max_length=50)
    view_link = models.CharField(max_length=500, unique=True)
    contributor = models.ForeignKey(to='users.User', on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    class Meta:
        db_table = 'video'

    @classmethod
    def get_videos(cls, sub_code: str) -> List:
        ''' Return List of video's whoose subject's code is sub_code.'''

        return cls.objects.filter(subject__code=sub_code, is_approved=True).values('name', 'view_link')

    @classmethod
    def total_not_verified(cls, user) -> int:
        '''Return total video tutorials contributed by user which is not approved.'''

        return len(cls.objects.filter(contributor=user, is_approved=False))

    def __str__(self) -> str:
        '''Str representation of VideoTutorial'''

        return self.name

class Syllabus(models.Model):

    ''' Model to store syllabus of each department and semester.'''

    department = models.ForeignKey(to=Department, on_delete=models.CASCADE, db_column='dept_name')
    semester = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])
    view_link = models.CharField(max_length=50)

    class Meta:
        db_table = 'syllabus'
    
    @classmethod
    def get_view_link(cls, dept_name: str, semester: int) -> List:
        '''Return list containing syllabus link of department whoose name is dept_name and semester.'''

        return cls.objects.filter(department__name=dept_name, semester=semester).values('view_link')

    def __str__(self) -> str:
        ''' Str representation of syllabus.'''

        return f'{self.department.name}(sem-{self.semester})'


class Topic(models.Model):

    ''' Store the topic names of subjects.'''

    name = models.CharField(max_length=50)
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE, db_column='sub_code')

    class Meta:
        db_table = 'topic'

        #A topic should belong to only one subject.
        unique_together = ['name', 'subject']

    def __str__(self) -> str:
        ''' Str representation of topic.'''

        return self.name



def validate_file_size(file, limit_mb = 50):
    ''' Validate a file's size does not exceed limit_mb.'''

    file_size = file.file.size
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError("Max size of file is %s MB" % limit_mb)



class Note(models.Model):

    ''' Store the note in pdf file of a topic.
    
    fields:\n
    topic - Foreign key to Topic model, represents note's topic.\n
    file - FileField, contain note's file.\n
    contributor - Foreign key to User model, represents note's contributor.\n
    is_approved- BoolField, status wheather note is approved or not.
    '''

    topic = models.ForeignKey(to=Topic, on_delete=models.CASCADE, db_column='topic_id')
    file = models.FileField(
        upload_to="notes/",
        validators=[FileExtensionValidator(allowed_extensions=['pdf','ppt','pptx','pptm','docx']),
         validate_file_size],
         db_column='view_link')
    contributor = models.ForeignKey(to='users.User', on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    class Meta:
        db_table = 'note'

        #An user must upload maximum one note of a topic.
        unique_together = ['topic', 'contributor']

    @classmethod
    def get_all_notes(cls, sub_code: str) ->List:
        ''' Get all notes whoose topic's subject's code is sub_code and return list of dict
        where each dict contain topic_name, contributor and view_link of note.
        '''

        notes_set= cls.objects.filter(topic__subject__code=sub_code, is_approved=True).order_by('topic__name')
        notes = []
        for note in notes_set:
            topic_name = note.topic.name
            contributor = f'{note.contributor.first_name} {note.contributor.last_name}'
            view_link = note.file.url
            notes.append({'topic_name':topic_name, 'contributor':contributor, 'view_link':view_link})
        return notes

    @classmethod
    def total_not_verified(cls, user) -> int:
        ''' Return total notes contributed by user which is not approved.'''

        return len(cls.objects.filter(contributor=user, is_approved=False))

    def __str__(self) -> str:
        ''' Str representation of note object.'''

        return self.topic.name



class QuestionPaper(models.Model):

    ''' Store the question paper in pdf file of a subject.
    
    fields:\n
    subject - Foreign key to Subject model, represents QuestionPaper's subject.\n
    year - IntegerField, year of question paper.\n
    file - FileField, contains QuestionPaper.\n
    contributor - Foreign key to User model, represents contributor.\n
    is_approved- BoolField, status wheather question paper is approved or not.
    '''
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE, db_column='sub_code')
    year = models.IntegerField(validators=[MinValueValidator(2015)])
    file = models.FileField(
        upload_to="question_Papers/",
        validators=[FileExtensionValidator(allowed_extensions=['pdf']),
         validate_file_size],
         db_column='view_link')
    contributor = models.ForeignKey(to='users.User', on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    class Meta:
        db_table = 'question_paper'

        #Exams of a subject happens only once in a year.
        unique_together = ['subject', 'year']

    @classmethod
    def get_question_papers(cls, sub_code: str) ->List:
        ''' Get the question papers whoose subject's code is sub_code and return a list of dict where 
        each dict contains information (year, contributor, link) of a question paper.
        '''
        
        question_set = cls.objects.filter(subject__code=sub_code, is_approved=True).order_by('-year')
        questions= []
        for question in question_set:
            year = question.year
            view_link = question.file.url
            contributor = f'{ question.contributor.first_name} {question.contributor.last_name}'
            questions.append({'year':year, 'contributor':contributor, 'view_link':view_link})
        return questions

    @classmethod
    def total_not_verified(cls, user) -> int:
        '''Return total Question Papers contributed by user which is not approved.'''

        return len(cls.objects.filter(contributor=user, is_approved=False))
    
    def __str__(self) -> str:
        ''' Str representation of QuestionPaper object.'''

        return self.subject.name




