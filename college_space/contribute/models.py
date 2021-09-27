from django.db import models
from users.models import User
from django.core.validators import validate_image_file_extension
import os
from django.core.exceptions import ValidationError

# Create your models here.
def validate_image(file):
    file_size = file.file.size
    limit_mb = 1
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError("Max size of file is %s MB" % limit_mb)

def ids_directory_path(instance, filename):
    f_name, extension = os.path.splitext(filename)
    user = instance.user.first_name + '( '+ instance.user.email +' )' + extension
    return 'college_ids/' + user

class Contributor(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    college_id = models.ImageField(
        upload_to= ids_directory_path,
        validators=[validate_image_file_extension],
        )

    def __str__(self) -> str:
        return self.user.first_name + '( ' + self.user.email +' )'
