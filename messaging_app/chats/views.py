# messaging_app/chats/views.py

from rest_framework import viewsets, filters
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id']

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with participants.
        Expected input:
        {
            "participants": [UUID1, UUID2]
        }
        """
        participant_ids = request.data.get('participants', [])
        if len(participant_ids) < 2:
            return Response({"error": "At least two participants are required."}, status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        conversation.participants.set(participant_ids)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        """
        Send a message to a conversation.
        Expected input:
        {
            "conversation_id": "<UUID>",
            "sender": "<UUID>",
            "message_body": "Hello!"
        }
        """
        data = request.data
        conversation_id = data.get("conversation_id")
        sender_id = data.get("sender")

        # Validate conversation
        conversation = get_object_or_404(Conversation, pk=conversation_id)

        # Validate sender
        sender = get_object_or_404(User, pk=sender_id)

        # Create message
        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=data.get("message_body", "")
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
