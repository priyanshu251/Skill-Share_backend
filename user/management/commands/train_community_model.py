import pandas as pd
from django.core.management.base import BaseCommand
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib

class Command(BaseCommand):
    help = "Train a model to predict trending communities"

    def handle(self, *args, **kwargs):
        # Load preprocessed data
        data = pd.read_csv("preprocessed_community_trend_data.csv")

        # Define features and target
        features = data[["session_count", "hours_spent", "new_members", "average_rating"]]
        target = data["trend_score"]

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

        # Initialize and train the model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Make predictions and evaluate the model
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        self.stdout.write(self.style.SUCCESS(f"Mean Squared Error: {mse}"))

        # Save the trained model
        joblib.dump(model, "community_trend_model.pkl")
        self.stdout.write(self.style.SUCCESS("Model saved as community_trend_model.pkl"))
