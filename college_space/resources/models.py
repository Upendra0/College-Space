from django.db import models
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.contrib import admin
from contribute.models import Contributor

department_type_choices = (
    ('cse', 'Computer Science & engineering'),
    ('ce', 'Civil engineering'),
    ('ee', 'Electrical engineering'),
    ('ece', 'Electronics and communication engineering'),
)


class Subject(models.Model):
    name = models.CharField(max_length=50)
    sub_code = models.CharField(max_length=12, unique=True)
    department = models.CharField(
        max_length=255, choices=department_type_choices)
    semester = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(8)])
    credit = models.FloatField(MinValueValidator(1))

    def __str__(self) -> str:
        return self.name

    @classmethod
    def get_subjects_list(cls, department=department, semester=semester):
        subject_lists = Subject.objects.filter(
            department=department, semester=semester)
        subjects = []
        for subject in subject_lists:
            subjects.append({'sub_code': subject.sub_code,
                            'name': subject.name, 'credit': subject.credit})
        return subjects


class Resource(models.Model):
    resource_type_choices = (
        ('book', 'Book'),
        ('video', 'Video Tutorial'),
        ('web', 'Web Tutorial'),
    )

    name = models.CharField(max_length=255)
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE)
    resource_type = models.CharField(
        max_length=10, choices=resource_type_choices)
    author = models.CharField(max_length=500)
    link = models.CharField(max_length=500)
    description = models.TextField()
    rating = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self) -> str:
        return self.subject.name + ' (' + self.resource_type + ')'

    @admin.display(description="Semester ")
    def get_semester(self):
        return self.subject.semester

    @admin.display(description="Department")
    def get_department(self):
        return self.subject.department

    @classmethod
    def get_vidoes_list(cls, sub_code):
        videos_list = cls.objects.filter(
            resource_type='video', subject__sub_code=sub_code)
        videos = []
        for video in videos_list:
            videos.append({'name': video.name, 'author': video.author,
                          'link': video.link, 'rating': video.rating})
        return videos

    @classmethod
    def get_books_list(cls, sub_code):
        books_list = cls.objects.filter(
            resource_type='book', subject__sub_code=sub_code)
        books = []
        for book in books_list:
            books.append({'name': book.name, 'author': book.author,
                          'link': book.link, 'rating': book.rating})
        return books

    @classmethod
    def get_web_list(cls, sub_code):
        web_list = cls.objects.filter(
            resource_type='web', subject__sub_code=sub_code
        )
        web_tutorials = []
        for web_tutorial in web_tutorials:
            web_tutorials.append({'name':web_tutorial.name, 'author': web_tutorial.author,
            'link': web_tutorial.link, 'rating': web_tutorial.rating})


class Syllabus(models.Model):
    department = models.CharField(
        max_length=255, choices=department_type_choices)
    semester = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(8)])
    download_link = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'syllabuse'

    def __str__(self) -> str:
        return self.department + '(sem-' + str(self.semester) + ')'

    @classmethod
    def get_syllabus_link(cls, department, semester):
        syllabus = cls.objects.filter(
            department=department, semester=semester).first()
        if syllabus is None:
            download_link = None
        else:
            download_link = syllabus.download_link
        return download_link


def notes_directory_path(instance, filename):
    user = instance.uploaded_by.user.first_name + \
        '_' + instance.uploaded_by.user.email
    new_file_name = instance.subject.name + \
        '( ' + instance.topic + ' )' + '.pdf'
    return 'Notes/' + user + '/' + new_file_name


class Note(models.Model):
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE)
    topic = models.CharField(max_length=50)
    file = models.FileField(upload_to=notes_directory_path, validators=[
                            FileExtensionValidator(allowed_extensions=['pdf'])])
    uploaded_by = models.ForeignKey(to=Contributor, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.subject.name + '( ' + self.topic + ' )'

    @classmethod
    def get_notes_list(cls, sub_code):
        notes_list = cls.objects.filter(subject__sub_code=sub_code)
        notes = {}
        for note in notes_list:
            user = note.uploaded_by.user.email
            temp_dict = {'topic': note.topic, 'url': note.file.url}
            if user in notes:
                notes[user].append(temp_dict)
            else:
                notes[user] = [temp_dict]
        return notes
