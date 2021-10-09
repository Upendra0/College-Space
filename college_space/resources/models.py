from django.db import models
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
import os
from django.core.exceptions import ValidationError

class Department(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    class Meta:
        db_table = 'department'

    @classmethod
    def all_department(cls):
        return cls.objects.all().values('name')

    def __str__(self) -> str:
        return self.name


class Subject(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=50)
    credit = models.FloatField(validators=[MinValueValidator(0)])

    class Meta:
        db_table = 'subject'

    def __str__(self) -> str:
        return self.name

class Taught(models.Model):
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE, db_column='sub_code')
    department = models.ForeignKey(to=Department, on_delete=models.CASCADE, db_column='dept_name')
    semester = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])

    class Meta:
        db_table = 'taught'
        unique_together = [['subject', 'department']]

    @classmethod
    def get_subjects(cls, dept_name, semester):
        # Returns the set of subjects taught in particular department in particular semester.
        return cls.objects.filter(department__name=dept_name, semester=semester).values('subject__code', 'subject__name', 'subject__credit')
        

    def __str__(self) -> str:
        return self.subject.name + self.department.name

class Book(models.Model):
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE, db_column='sub_code')
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    view_link = models.CharField(max_length=500)
    contributor = models.ForeignKey(to='users.User', on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    class Meta:
        db_table = 'book'

    def __str__(self) -> str:
        return self.name

    @classmethod
    def get_books(cls, sub_code):
        return cls.objects.filter(subject__code=sub_code, is_approved=True).values('name', 'author', 'view_link')

class WebTutorial(models.Model):
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE, db_column='sub_code')
    name = models.CharField(max_length=50)
    view_link = models.CharField(max_length=500)
    contributor = models.ForeignKey(to='users.User', on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    class Meta:
        db_table = 'web_tutorial'

    @classmethod
    def get_web_tutorials(cls, sub_code):
        return cls.objects.filter(subject__code=sub_code, is_approved=True).values('name', 'view_link')

    def __str__(self) -> str:
        return self.name

class Video(models.Model):
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE, db_column='sub_code')
    name = models.CharField(max_length=50)
    view_link = models.CharField(max_length=500)
    contributor = models.ForeignKey(to='users.User', on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    class Meta:
        db_table = 'video'

    @classmethod
    def get_books(cls, sub_code):
        return cls.objects.filter(subject__code=sub_code, is_approved=True).values('name', 'view_link')

    def __str__(self) -> str:
        return self.name

class Syllabus(models.Model):
    department = models.ForeignKey(to=Department, on_delete=models.CASCADE, db_column='dept_name')
    semester = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])
    view_link = models.CharField(max_length=255)

    class Meta:
        db_table = 'syllabus'
    
    @classmethod
    def get_view_link(cls, dept_name, semester):
        return cls.objects.filter(department__name=dept_name, semester=semester).values('view_link')
        
    def __str__(self) -> str:
        return self.department.name + '(sem-' + str(self.semester) + ')'


class Topic(models.Model):
    name = models.CharField(max_length=50)
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE, db_column='sub_code')

    class Meta:
        db_table = 'topic'

    def __str__(self) -> str:
        return self.name



def validate_file_size(file):
    file_size = file.file.size
    limit_mb = 15
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError("Max size of file is %s MB" % limit_mb)


def notes_directory_path(instance, filename):
    user = instance.contributor.email
    f_name, extension = os.path.splitext(filename)
    new_file_name =  instance.topic.name + extension
    return 'Notes/' + user + '/' + new_file_name


class Note(models.Model):
    topic = models.ForeignKey(to=Topic, on_delete=models.CASCADE, db_column='topic_id')
    file = models.FileField(
        upload_to=notes_directory_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf']),
         validate_file_size],
         db_column='view_link')
    contributor = models.ForeignKey(to='users.User', on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.topic.name

def question_directory_path(instance, filename):
    user = instance.contributor.email
    f_name, extension = os.path.splitext(filename)
    new_file_name =  instance.subject.name + extension
    return 'Question_Papers/' + user + '/' + new_file_name

class QuestionPaper(models.Model):
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE, db_column='sub_code')
    year = models.IntegerField(validators=[MinValueValidator(2015)])
    file = models.FileField(
        upload_to=question_directory_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf']),
         validate_file_size],
         db_column='view_link')
    contributor = models.ForeignKey(to='users.User', on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    class Meta:
        db_table = 'question_paper'

    def __str__(self) -> str:
        return self.subject.name

    @classmethod
    def get_question_papers(cls, sub_code):
        query_set = cls.objects.filter(sub_code=sub_code, is_approved=True).values('year', 'file').order_by('-year')
        return query_set




