''' Signal to auto delete user's profile pic.'''

from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

from .models import User

@receiver(pre_save, sender=User)
def delete_file_on_update(sender, instance, **kwargs):

    """
    Delete the user's old profile pic file when user update the profile and return the status
    True or False i.e where old pic is deleted or not.
    """

    # If instance is saving for first time in database, don't delete profile_pic file.    
    try:
        old_file = sender.objects.get(pk=instance.pk).profile_pic
    except sender.DoesNotExist:
        return False

    # If user has not updated profile pic, don't delete profile_pic file.
    new_file = instance.profile_pic
    if old_file == new_file:
        return False
    
    try:
        old_file.delete(save=False)
    except Exception:
        return False
    else:
        return True

@receiver(post_delete, sender=User)
def delete_file_on_model_delete(sender, instance, **kwargs):
    
    """
    Delete the user's profile pic file when a user instance is deleted and return a status True or
    False i.e wheteher pic is deleted or not.
    """

    # Can't remove the profile_pic as instance does'nt has one.
    if not instance.profile_pic:
        return False

    try:
        instance.profile_pic.delete(save=False)
    except Exception:
        return False
    else:
        return True