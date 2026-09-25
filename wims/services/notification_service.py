"""Notification use cases."""
from ..domain.entities import Notification
from ..repositories.base import BaseRepository


class NotificationService:
    """Read and update inbox notifications."""
    def __init__(self, notifications: BaseRepository[Notification]):
        self.notifications = notifications

    def list_all(self) -> list[Notification]:
        return self.notifications.list()

    def mark_all_read(self) -> None:
        for item in self.notifications.list():
            item.unread = False
            self.notifications.update(item)
