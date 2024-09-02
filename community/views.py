from django.http import JsonResponse
from django.views import View
import joblib
import pandas as pd
from rest_framework import generics, permissions, authentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from skill_share.authentication import FirebaseAuthentication
from community.models import Skill
from community.serializers import (
    SkillSerializer,
    CommunitySerializer,
    CommunityListSerializer,
    SessionSerializer,
    FeedbackSerializer,
)

from community.services.community_service import CommunityService

community_service = CommunityService()


class SkillListCreateView(generics.ListCreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    authentication_classes = [FirebaseAuthentication]


class CommunityListCreateView(APIView):
    authentication_classes = [FirebaseAuthentication]

    def post(self, request):
        data = request.data
        community = community_service.create_new_community(data=data, user=request.user)
        return Response(
            CommunitySerializer(community).data, status=status.HTTP_201_CREATED
        )

    def get(self, request):
        communities = community_service.get_all_communities()
        return Response(
            CommunityListSerializer(
                communities, many=True, context={"request": request}
            ).data,
            status=status.HTTP_200_OK,
        )


class SessionView(APIView):
    authentication_classes = [FirebaseAuthentication]

    def post(self, request):
        try:
            data = request.data
            print(data)
            session = community_service.create_new_session_for_community(data)
            return Response(session, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        community = request.query_params.get("community")
        sessions = community_service.get_sessions(community)
        return Response(sessions, status=status.HTTP_200_OK)


class FeedbackView(APIView):
    authentication_classes = [FirebaseAuthentication]

    def post(self, request):
        try:
            data = request.data
            user = request.user
            data["user"] = user.pk
            feedback = community_service.give_feedback(data)
            return Response(feedback, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        session = request.query_params.get("session")
        feedback = community_service.get_feedback(session)
        return Response(feedback, status=status.HTTP_200_OK)


class CommunityMembersView(APIView):
    authentication_classes = [FirebaseAuthentication]

    def post(self, request):
        try:
            data = request.data
            community_name = data.get("community")
            members = [request.user]
            community = community_service.add_members_to_community(
                community_name, members
            )
            return Response(
                CommunitySerializer(community).data, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PredictSessionView(View):
    def get(self, request):
        # Example: /predict?community=CommunityName&time=2023-06-01T14:00:00&duration=60
        community = request.GET.get("community")
        time = request.GET.get("time")
        duration = int(request.GET.get("duration"))

        time = pd.to_datetime(time)
        hour = time.hour
        day_of_week = time.dayofweek

        # Load the trained model
        model = joblib.load("community/trained_model.joblib")

        # Predict
        features = pd.DataFrame(
            [[community, hour, day_of_week, duration]],
            columns=["community", "hour", "day_of_week", "duration"],
        )
        predicted_rating = model.predict(features)[0]

        return JsonResponse({"predicted_rating": predicted_rating})
