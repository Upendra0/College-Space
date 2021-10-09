# Generated by Django 3.2.6 on 2021-10-08 18:43

import django.core.validators
from django.db import migrations, models
import resources.models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0002_alter_department_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='file',
            field=models.FileField(db_column='view_link', upload_to=resources.models.notes_directory_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf']), resources.models.validate_file_size]),
        ),
        migrations.AlterField(
            model_name='questionpaper',
            name='file',
            field=models.FileField(db_column='view_link', upload_to=resources.models.question_directory_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf']), resources.models.validate_file_size]),
        ),
        migrations.AlterUniqueTogether(
            name='taught',
            unique_together={('subject', 'department')},
        ),
    ]