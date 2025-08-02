from django.contrib.auth.models import User  # type: ignore
from .models import Message, Notification, MessageHistory
from django.db.models.signals import post_delete  # type: ignore
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


@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    # Delete messages sent or received by the user
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications for the user
    Notification.objects.filter(user=instance).delete()

    # Delete any message history related to their messages
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()
