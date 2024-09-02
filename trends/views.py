from django.http import JsonResponse
from django.views import View
import pandas as pd
import joblib
from datetime import datetime
from community.models import Session, TimeBank, Skill, Membership, Feedback


class SkillTrendView(View):
    model = joblib.load("skill_trend_model.pkl")

    def collect_data(self):
        sessions = Session.objects.all().values("community__skill__name", "time")
        session_data = pd.DataFrame(list(sessions))

        time_banks = TimeBank.objects.all().values(
            "user__uid", "hours_spent", "user__memberships__community__skill__name"
        )
        time_bank_data = pd.DataFrame(list(time_banks))

        memberships = Membership.objects.all().values(
            "user__uid", "community__skill__name", "date_joined"
        )
        membership_data = pd.DataFrame(list(memberships))

        feedbacks = Feedback.objects.all().values(
            "session__community__skill__name", "rating"
        )
        feedback_data = pd.DataFrame(list(feedbacks))

        return session_data, time_bank_data, membership_data, feedback_data

    def preprocess_data(
        self, session_data, time_bank_data, membership_data, feedback_data
    ):
        session_data["time"] = pd.to_datetime(session_data["time"])
        session_data["year_month"] = session_data["time"].dt.to_period("M")
        session_count = (
            session_data.groupby(["community__skill__name", "year_month"])
            .size()
            .reset_index(name="session_count")
        )

        time_bank_data["community__skill__name"] = time_bank_data[
            "user__memberships__community__skill__name"
        ]
        time_spent = (
            time_bank_data.groupby("community__skill__name")["hours_spent"]
            .sum()
            .reset_index()
        )

        membership_data["date_joined"] = pd.to_datetime(membership_data["date_joined"])
        membership_data["year_month"] = membership_data["date_joined"].dt.to_period("M")
        membership_growth = (
            membership_data.groupby(["community__skill__name", "year_month"])
            .size()
            .reset_index(name="new_members")
        )

        feedback_score = (
            feedback_data.groupby("session__community__skill__name")["rating"]
            .mean()
            .reset_index(name="average_rating")
        )

        combined_data = session_count.merge(
            time_spent,
            left_on="community__skill__name",
            right_on="community__skill__name",
            how="left",
        )
        combined_data = combined_data.merge(
            membership_growth,
            left_on=["community__skill__name", "year_month"],
            right_on=["community__skill__name", "year_month"],
            how="left",
        )
        combined_data = combined_data.merge(
            feedback_score,
            left_on="community__skill__name",
            right_on="session__community__skill__name",
            how="left",
        )

        combined_data = combined_data.fillna(0)

        return combined_data

    def get(self, request, *args, **kwargs):
        session_data, time_bank_data, membership_data, feedback_data = (
            self.collect_data()
        )
        combined_data = self.preprocess_data(
            session_data, time_bank_data, membership_data, feedback_data
        )
        features = combined_data[
            ["session_count", "hours_spent", "new_members", "average_rating"]
        ]
        predictions = self.model.predict(features)
        combined_data["trend_score"] = predictions
        combined_data.drop_duplicates(
            subset=["community__skill__name"], inplace=True
        )  # Ensure unique skills
        emerging_skills = combined_data.sort_values(
            by="trend_score", ascending=False
        ).head(10)
        response_data = emerging_skills[
            ["community__skill__name", "trend_score"]
        ].to_dict(orient="records")
        return JsonResponse(response_data, safe=False)





class CommunityTrendView(View):
    model = joblib.load("community_trend_model.pkl")
    
    def collect_data(self):
        sessions = Session.objects.all().values("community__name", "time", "duration")
        session_data = pd.DataFrame(list(sessions))

        time_banks = TimeBank.objects.all().values("user__uid", "hours_spent", "user__memberships__community__name")
        time_bank_data = pd.DataFrame(list(time_banks))

        memberships = Membership.objects.all().values("user__uid", "community__name", "date_joined")
        membership_data = pd.DataFrame(list(memberships))

        feedbacks = Feedback.objects.all().values("session__community__name", "rating")
        feedback_data = pd.DataFrame(list(feedbacks))

        return session_data, time_bank_data, membership_data, feedback_data

    def preprocess_data(self, session_data, time_bank_data, membership_data, feedback_data):
        session_data["time"] = pd.to_datetime(session_data["time"])
        session_data["year_month"] = session_data["time"].dt.to_period("M")
        session_count = session_data.groupby(["community__name", "year_month"]).size().reset_index(name="session_count")

        time_bank_data["community__name"] = time_bank_data["user__memberships__community__name"]
        time_spent = time_bank_data.groupby("community__name")["hours_spent"].sum().reset_index()

        membership_data["date_joined"] = pd.to_datetime(membership_data["date_joined"])
        membership_data["year_month"] = membership_data["date_joined"].dt.to_period("M")
        membership_growth = membership_data.groupby(["community__name", "year_month"]).size().reset_index(name="new_members")

        feedback_score = feedback_data.groupby("session__community__name")["rating"].mean().reset_index(name="average_rating")

        combined_data = session_count.merge(time_spent, on="community__name", how="left")
        combined_data = combined_data.merge(membership_growth, on=["community__name", "year_month"], how="left")
        combined_data = combined_data.merge(feedback_score, left_on="community__name", right_on="session__community__name", how="left")

        combined_data = combined_data.fillna(0)

        return combined_data

    def get(self, request, *args, **kwargs):
        session_data, time_bank_data, membership_data, feedback_data = self.collect_data()
        combined_data = self.preprocess_data(session_data, time_bank_data, membership_data, feedback_data)
        features = combined_data[["session_count", "hours_spent", "new_members", "average_rating"]]
        predictions = self.model.predict(features)
        combined_data["trend_score"] = predictions
        combined_data.drop_duplicates(subset=["community__name"], inplace=True)  # Ensure unique communities
        trending_communities = combined_data.sort_values(by="trend_score", ascending=False).head(10)
        response_data = trending_communities[["community__name", "trend_score"]].to_dict(orient="records")
        return JsonResponse(response_data, safe=False)
