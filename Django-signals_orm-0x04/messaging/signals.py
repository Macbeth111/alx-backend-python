from django.db.models.signals import post_save  # type: ignore
from django.dispatch import receiver  # type: ignore
from .models import Message, Notification


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    # This means the message already exists (i.e., update not create)
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:
                # Save old content to history
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_message.content
                )
                # Mark as edited
                instance.edited = True
        except Message.DoesNotExist:
            pass
