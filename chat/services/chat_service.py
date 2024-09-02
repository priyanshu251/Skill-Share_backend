from chat.models import Chat
from chat.repositories.chat_repository import ChatRepository
from chat.serializers import ChatSerializer


class ChatService:
    def __init__(self, repository: ChatRepository) -> None:
        self.repository = repository

    def create_new_chat(self, data: dict):
        document_id = self.repository.create_new_chat_in_firestore(data=data)
        participants = data["participants"]
        data.pop("participants")
        self.repository.create_new_chat_in_database(document_id=document_id, data=data)
        chat = self.repository.add_participants_to_chat(
            document_id=document_id, participants=participants
        )
        return ChatSerializer(chat).data

    def add_participants_to_chat(self, document_id, participants):
        return self.repository.add_participants_to_chat(
            document_id=document_id, participants=participants
        )

    def get_or_create_chat(self, data: dict):
        chat = self.repository.get_dm_chat(participants=data["participants"])
        if not chat:
            return self.create_new_chat(data=data)
        return ChatSerializer(chat).data

    def get_all_dms_for_user(self, user):
        return ChatSerializer(
            self.repository.get_all_dms_for_user(user), many=True
        ).data
    
    def update_last_message_time(self, document_id):
        return ChatSerializer(self.repository.update_last_message_time(document_id=document_id)).data
