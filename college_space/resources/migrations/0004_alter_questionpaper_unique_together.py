# Generated by Django 3.2.6 on 2021-10-09 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0003_auto_20211009_0013'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='questionpaper',
            unique_together={('subject', 'year')},
        ),
    ]
