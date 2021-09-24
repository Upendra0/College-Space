from django.db import models
from django.core.validators import  MaxLengthValidator, MinLengthValidator, MinValueValidator, MaxValueValidator
from django.contrib import admin

department_type_choices = (
    ('cse', 'Computer Science & engineering'),
    ('ce', 'Civil engineering'),
    ('ee', 'Electrical engineering'),
    ('ece', 'Electronics and communication engineering'),
)


class Subject(models.Model):
    name = models.CharField(max_length=50)
    sub_code= models.CharField(max_length=12)
    department = models.CharField( max_length=255, choices=department_type_choices)
    semester = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])
    credit = models.FloatField()
    
    def __str__(self) -> str:
        return self.name


class Resource(models.Model):
    resource_type_choices = (
        ('book', 'Book'),
        ('video', 'Video Tutorial'),
        ('web', 'Web Tutorial'),
    )

    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE)
    resource_type = models.CharField(max_length=10, choices=resource_type_choices)
    author = models.CharField(max_length=500)
    link = models.CharField(max_length=500)
    description = models.TextField()
    rating = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self) -> str:
        return self.subject.name + ' (' + self.resource_type + ')'

    @admin.display(description="Semester ")
    def get_semester(self):
        return self.subject.semester

    @admin.display(description="Department")
    def get_department(self):
        return self.subject.department


class Syllabus(models.Model):
    department = models.CharField( max_length=255, choices=department_type_choices)
    semester = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])
    download_link = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'syllabuse'

    def __str__(self) -> str:
        return self.department + '(sem-' + str(self.semester) + ')'
