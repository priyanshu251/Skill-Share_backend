from rest_framework import serializers
from django.db.models import Avg

from community.models import (
    Skill,
    Community,
    Membership,
    Badge,
    Session,
    Feedback,
    TimeBank,
    Project,
)


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = "__all__"


class CommunityListSerializer(serializers.ModelSerializer):
    is_admin = serializers.SerializerMethodField()
    is_member = serializers.SerializerMethodField()
    skill = SkillSerializer()

    class Meta:
        model = Community
        fields = "__all__"

    def get_is_admin(self, obj):
        if Membership.objects.filter(
            user=self.context["request"].user, community=obj
        ).exists():
            return Membership.objects.get(
                user=self.context["request"].user, community=obj
            ).is_admin
        else:
            return False

    def get_is_member(self, obj):
        return Membership.objects.filter(
            user=self.context["request"].user, community=obj
        ).exists()
    
class SessionSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = "__all__"

    def get_rating(self, obj):
        return Feedback.objects.filter(session=obj).aggregate(
            rating=Avg("rating")
        )["rating"]
    
class SessionCreateSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = "__all__"

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"
