import pandas as pd
from django.core.management.base import BaseCommand
from community.models import Session, TimeBank, Skill, Membership, Feedback
from datetime import datetime


class Command(BaseCommand):
    help = "Collect and preprocess data for skill trend prediction"

    def handle(self, *args, **kwargs):
        def collect_data():
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
            session_data, time_bank_data, membership_data, feedback_data
        ):
            # Processing session data
            session_data["time"] = pd.to_datetime(session_data["time"])
            session_data["year_month"] = session_data["time"].dt.to_period("M")
            session_count = (
                session_data.groupby(["community__skill__name", "year_month"])
                .size()
                .reset_index(name="session_count")
            )

            # Processing time bank data
            time_bank_data["community__skill__name"] = time_bank_data[
                "user__memberships__community__skill__name"
            ]
            time_spent = (
                time_bank_data.groupby("community__skill__name")["hours_spent"]
                .sum()
                .reset_index()
            )

            # Processing membership data
            membership_data["date_joined"] = pd.to_datetime(
                membership_data["date_joined"]
            )
            membership_data["year_month"] = membership_data["date_joined"].dt.to_period(
                "M"
            )
            membership_growth = (
                membership_data.groupby(["community__skill__name", "year_month"])
                .size()
                .reset_index(name="new_members")
            )

            # Processing feedback data
            feedback_score = (
                feedback_data.groupby("session__community__skill__name")["rating"]
                .mean()
                .reset_index(name="average_rating")
            )

            # Combining all data
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

        session_data, time_bank_data, membership_data, feedback_data = collect_data()
        combined_data = preprocess_data(
            session_data, time_bank_data, membership_data, feedback_data
        )

        # Save preprocessed data to a CSV file or database for later use
        combined_data.to_csv("preprocessed_skill_trend_data.csv", index=False)

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully collected and preprocessed data for skill trend prediction"
            )
        )
