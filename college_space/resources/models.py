from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=50)
    syllabus = models.CharField(max_length=500)
    semester = models.SmallIntegerField()
    credit = models.SmallIntegerField()

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
    rating = models.SmallIntegerField()