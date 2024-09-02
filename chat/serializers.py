from rest_framework import serializers
from chat.models import Chat
from user.serializers import UserSerializer


class ChatSerializer(serializers.ModelSerializer):
    participants = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Chat
        fields = "__all__"
