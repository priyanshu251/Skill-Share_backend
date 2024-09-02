from sklearn.cluster import KMeans
import pandas as pd
import joblib
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Train the model for predicting skill trends"

    def handle(self, *args, **kwargs):
        def train_model():
            # Load preprocessed data
            data = pd.read_csv("preprocessed_skill_trend_data.csv")
            features = data[
                ["session_count", "hours_spent", "new_members", "average_rating"]
            ]

            # Train KMeans clustering model
            model = KMeans(n_clusters=5)
            model.fit(features)

            # Save the model
            joblib.dump(model, "skill_trend_model.pkl")

            self.stdout.write(
                self.style.SUCCESS(
                    "Successfully trained and saved the skill trend model"
                )
            )

        train_model()
