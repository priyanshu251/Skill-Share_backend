from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from typing import List

from skill_share.authentication import FirebaseAuthentication
from chat.repositories.chat_repository import ChatRepository
from chat.services.chat_service import ChatService

from user.models import User

chatService = ChatService(repository=ChatRepository())


class ChatListCreateView(APIView):
    authentication_classes = [FirebaseAuthentication]

    def post(self, request):
        data = request.data
        user: User = request.user
        participants = data["participants"]
        participants.append(user.uid)
        data["participants"] = participants
        return Response(
            chatService.get_or_create_chat(data=data), status=status.HTTP_200_OK
        )

    def get(self, request):
        user: User = request.user
        return Response(
            chatService.get_all_dms_for_user(user=user), status=status.HTTP_200_OK
        )

    def patch(self, request):
        data = request.data
        document_id = data["document_id"]
        return Response(
            chatService.update_last_message_time(document_id=document_id),
            status=status.HTTP_200_OK,
        )
