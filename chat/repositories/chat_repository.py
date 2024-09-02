from django.db.models import Count, Case, When
import firebase_admin.firestore
from chat.models import Chat
import firebase_admin


class ChatRepository:
    def create_new_chat_in_firestore(self, data):
        client = firebase_admin.firestore.client()
        chat_collection = client.collection("chats")
        timestamp, document_ref = chat_collection.add(data)
        print(timestamp)
        print(document_ref.id)
        return document_ref.id

    def create_new_chat_in_database(self, data, document_id):
        return Chat.objects.create(document_id=document_id, **data)

    def add_participants_to_chat(self, document_id, participants):
        chat = Chat.objects.get(pk=document_id)
        chat.participants.add(*participants)
        return chat

    def get_chat_by_participants(self, participants):
        return Chat.objects.filter(participants__in=participants).distinct()

    def get_dm_chat(self, participants):
        # chats = (
        #     Chat.objects.filter(type="dm", participants__in=participants)
        #     .annotate(
        #         matching_participants=Count(
        #             Case(When(participants__in=participants, then=1))
        #         )
        #     )
        #     .filter(matching_participants=len(participants))
        #     .distinct()
        # )
        chats = Chat.objects.filter(type="dm", participants__in=participants).distinct()
        chats = chats.annotate(
            matching_participants=Count(
                Case(When(participants__in=participants, then=1))
            )
        )
        chats = chats.filter(matching_participants=len(participants))
        print(chats)
        if chats.exists():
            return Chat.objects.get(pk=chats.first().document_id)
        else:
            return None

    def get_all_dms_for_user(self, user):
        return Chat.objects.filter(type="dm", participants=user).order_by(
            "-last_message_time"
        )

    def update_last_message_time(self, document_id):
        chat = Chat.objects.get(pk=document_id)
        chat.save()
        return chat
        
