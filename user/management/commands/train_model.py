import pandas as pd
from django.core.management.base import BaseCommand
from django.utils import timezone
from sklearn.discriminant_analysis import StandardScaler
from community.models import Session, Feedback, Community, Membership
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
from django.db.models import Avg

class Command(BaseCommand):
    help = 'Train the session prediction model'

    def handle(self, *args, **kwargs):
        # Collect data from the database
        sessions = Session.objects.all()
        feedbacks = Feedback.objects.all()

        data = []
        for session in sessions:
            feedbacks_for_session = feedbacks.filter(session=session)
            avg_rating = feedbacks_for_session.aggregate(Avg('rating'))['rating__avg']
            num_feedbacks = feedbacks_for_session.count()

            data.append({
                'session_id': session.id,
                'community': session.community.name,  # Use community name or ID
                'time': session.time,
                'duration': session.duration,
                'avg_rating': avg_rating,
                'num_feedbacks': num_feedbacks,
            })

        df = pd.DataFrame(data)
        if df.shape[0] < 2:
            self.stdout.write(self.style.ERROR('Not enough data to train the model.'))
            return

        # Preprocess data (e.g., extract features like hour of the day, day of the week)
        df['hour'] = df['time'].dt.hour
        df['day_of_week'] = df['time'].dt.dayofweek

        print(df)

        # Define features and target
        features = ['community', 'hour', 'day_of_week', 'duration']
        target = 'avg_rating'

        X = df[features]
        y = df[target]

        print(y)

        X = X[y.notna()]
        y = y[y.notna()]

        # One-hot encode the community feature
        numeric_features = ['duration', 'hour', 'day_of_week']
        numeric_transformer = StandardScaler()

        categorical_features = ['community']
        categorical_transformer = OneHotEncoder(handle_unknown='ignore')

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)
            ])

        # Define the model pipeline
        model = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('regressor', RandomForestRegressor())
        ])

        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the model
        model.fit(X_train, y_train)

        # Evaluate the model
        y_pred = model.predict(X_test)
        rmse = mean_squared_error(y_test, y_pred, squared=False)
        self.stdout.write(self.style.SUCCESS(f'RMSE: {rmse}'))

        # Save the model
        joblib.dump(model, 'community/trained_model.joblib')
        self.stdout.write(self.style.SUCCESS('Model training complete and saved.'))
