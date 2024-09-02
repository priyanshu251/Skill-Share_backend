from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise import accuracy

def prepare_data(interaction_matrix):
    reader = Reader(rating_scale=(-1, 3))
    data = Dataset.load_from_df(interaction_matrix.stack().reset_index(), reader)
    trainset, testset = train_test_split(data, test_size=0.2)
    return trainset, testset

def train_model(trainset):
    model = SVD()
    model.fit(trainset)
    return model

def evaluate_model(model, testset):
    predictions = model.test(testset)
    accuracy.rmse(predictions)

def recommend_posts(model, user_id, interaction_matrix, top_n=10):
    user_ratings = interaction_matrix.loc[user_id].values
    user_interactions = {post_id: rating for post_id, rating in enumerate(user_ratings) if rating != 0}

    all_post_ids = set(interaction_matrix.columns)
    seen_post_ids = set(user_interactions.keys())
    unseen_post_ids = list(all_post_ids - seen_post_ids)

    predictions = [model.predict(user_id, post_id) for post_id in unseen_post_ids]
    recommendations = sorted(predictions, key=lambda x: x.est, reverse=True)[:top_n]
    
    return [rec.iid for rec in recommendations]
