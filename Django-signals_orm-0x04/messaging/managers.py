from django.db import models  # type: ignore


class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        return self.filter(receiver=user, read=False).only('sender', 'content', 'timestamp')
