from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import Note, QuestionPaper

@receiver(pre_save)
def delete_file_on_update(sender, instance, **kwargs):

    """
    Delete the instance's old file when instance's file field is updated and return the status
    True or False i.e where old file is deleted or not.
    """

    #Delete if instance belong to one of following models
    file_models = [Note, QuestionPaper]
    if sender not in file_models:
        return False

    # If instance is saving for first time in database, don't delete file.    
    try:
        old_file = sender.objects.get(pk=instance.pk).file
    except sender.DoesNotExist:
        return False

    # If instance has not updated file, don't delete file.
    new_file = instance.file
    if old_file == new_file:
        return False
    
    try:
        old_file.delete(save=False)
        return True
    except Exception:
        return False

@receiver(post_delete)
def delete_file_on_model_delete(sender, instance, **kwargs):

    """
    Delete the  file when a  instance is deleted and return a status True or
    False i.e wheteher file is deleted or not.
    """

    #Delete if instance belong to one of following models
    file_models = [Note, QuestionPaper]
    if sender not in file_models:
        return False


    # Can't remove the file as instance does'nt has one.
    if not instance.file:
        return False

    try:
        instance.file.delete(save=False)
        return True
    except Exception:
        return False