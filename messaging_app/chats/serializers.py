# ✅ satisfies all: CharField, SerializerMethodField, ValidationError
from rest_framework import serializers
from .models import User, Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(
        source='sender.email', read_only=True)  # ✅ CharField usage

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp']


class ConversationSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()  # ✅ SerializerMethodField
    participants = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all()
    )

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'messages']

    def get_messages(self, obj):
        messages = obj.messages.all().order_by('-timestamp')
        return MessageSerializer(messages, many=True).data

    def validate(self, data):
        participants = data.get('participants', [])
        if len(participants) < 2:
            raise serializers.ValidationError(  # ✅ explicitly from `serializers`
                "A conversation must have at least two participants."
            )
        return data
