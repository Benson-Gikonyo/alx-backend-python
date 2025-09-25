from django.shortcuts import render
from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from .models import User, Conversation, Message
from .serializers import MessageSerializer, ConversationSerializer #UserSerializer,

# Create your views here.
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["participants_id__first_name", "participants_id__last_name"]

    def createConversation(self,request, *args, **kwargs):
        """Create conversation. Expects participant_id"""

        participant_id = request.data.get("participants_id")

        if not participant_id:
            return Response(
                {"error": "participants id is required"}
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            participant = User.objects.get(pk=participant_id)

        except User.DoesNotExist:
            return Response(
                {"Error:": "Invalid participant_id"}
                status=status.HTTP_404_NOT_FOUND,
            )
        
        conversation = Conversation.objects.create(participant_id=participant)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

        def perform_create (self, serializer):
            serializer.save()
    

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["message_body"]

    def createMessage(self, request, *args, **kwargs):
        """create and send a message in an existing conversation
        Expects sender_id, conversation_id, and message_body
        """

        sender_id = request.data.get("sender_id")
        conversation_id = request.data.get("conversation_id")
        message_body  = request.data.get("message_body")

        if not sender_id or not conversation_id or not message_body:
            return Response(
                {"Error:": "Sender_id, conversation_id and message_body are required"}
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        try:
            sender = User.objects.get(pk=sender_id)
        except  User.DoesNotExist:
            return Response(
                {"Error: ": "Invalid sender_id"}
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            conversation = Conversation.objects.get(pk=conversation_id)
        except  Conversation.DoesNotExist:
            return Response(
                {"Error: ": "Invalid conversation_id"}
                status=status.HTTP_404_NOT_FOUND
            )
        
        message = Message.objects.create(
            sender_id=sender,
            message_body=message_body,
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def perform_create(self, serializer):
        serializer.save()
    