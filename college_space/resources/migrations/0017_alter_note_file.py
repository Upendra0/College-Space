# Generated by Django 3.2.6 on 2021-09-27 14:07

import django.core.validators
from django.db import migrations, models
import resources.models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0016_alter_note_uploaded_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='file',
            field=models.FileField(upload_to=resources.models.notes_directory_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'JPEG', 'JPG', 'PNG'])]),
        ),
    ]
