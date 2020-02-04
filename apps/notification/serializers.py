from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Notification


class NotificationSerializer(ModelSerializer):
    from_user_username = SerializerMethodField('_from_user_username', read_only=True)
    to_user_username = SerializerMethodField('_to_user_username', read_only=True)

    @staticmethod
    def _from_user_username(notification: Notification):
        return notification.from_user.username

    @staticmethod
    def _to_user_username(notification: Notification):
        return notification.to_user.username

    class Meta:
        model = Notification
        fields = ['from_user_username', 'to_user_username', 'message', 'target_id', 'type']
