import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Media

@receiver(post_delete, sender=Media)
def delete_media_file(sender, instance, **kwargs):
    """
    Deletes file from filesystem when corresponding Media object is deleted.
    """
    if instance.file and os.path.isfile(instance.file.path):
        os.remove(instance.file.path)

@receiver(pre_save, sender=Media)
def delete_old_file_on_update(sender, instance, **kwargs):
    """
    Deletes old file from filesystem when a new file is assigned to the file field.
    """
    if not instance.pk:
        # No primary key means this is a new object, nothing to delete
        return

    try:
        old_instance = Media.objects.get(pk=instance.pk)
    except Media.DoesNotExist:
        return

    old_file = old_instance.file
    new_file = instance.file

    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
