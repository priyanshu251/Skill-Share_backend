from user.models import User
from user.serializers import UserSerializer
from rest_framework import serializers
from django.db.models import Q


class UserRepository:
    def create_new_user(self, data):
        serializer = UserSerializer(data=data)
        # serializer.validate()
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def get_user_from_firebase_uid(self, uid: str):
        try:
            user = User.objects.get(pk=uid)
            return user
        except User.DoesNotExist:
            return None

    def search_user_by_name_and_email(self, search_query, user):
        users = User.objects.filter(
            Q(name__icontains=search_query) | Q(email__icontains=search_query)
        ).exclude(pk=user)
        serializer = UserSerializer(users, many=True)
        return serializer.data
