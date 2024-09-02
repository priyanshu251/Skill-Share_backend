from user.models import User
from community.models import (
    Skill,
    Community,
    Badge,
    Session,
    Membership,
    Feedback,
    TimeBank,
    Project,
)
from community.serializers import (
    SkillSerializer,
    CommunitySerializer,
    CommunityListSerializer,
    SessionSerializer,
    SessionCreateSerializer,
    FeedbackSerializer,
)


class CommunityRepository:
    def create_new_community(self,data):
        serializer = CommunitySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    # here is_admin data can also be passed
    def add_members_to_community(self, name, members):
        community = Community.objects.get(pk=name)
        community.members.add(*members)
        return community

    def make_admin(self, community, user):
        membership = Membership.objects.get(user=user, community=community)
        membership.is_admin = True
        membership.save()
        return membership

    def create_new_badge(self, data):
        return Badge.objects.create(**data)

    def update_badge_level(self, user, skill, dec=False):
        if Badge.objects.get(user=user, skill=skill) is not None:
            badge = Badge.objects.get(user=user, skill=skill)
            if dec:
                badge.level = max(0, badge.level - 1)
            else:
                badge.level = badge.level + 1
            badge.save()
            return badge

    def get_all_communities(self):
        return Community.objects.all()

    def create_new_session_for_community(self, data):
        serializer = SessionCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def give_feedback(self, data):
        serializer = FeedbackSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def get_sessions(self, community):
        return SessionSerializer(Session.objects.filter(community=community), many=True).data

    def get_feedback(self, session):
        return FeedbackSerializer(Feedback.objects.filter(session=session), many=True).data
