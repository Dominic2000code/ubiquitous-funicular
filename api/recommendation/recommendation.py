# source : https://medium.com/@apokolipsu/building-recommendation-algorithms-for-social-media-platforms-1033de5515d0
import os
import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds
from scipy.sparse import csr_matrix
from django.conf import settings

# Load the data
# Load your user, post, and likes data into pandas DataFrames
csv_directory = os.path.join(settings.BASE_DIR, 'api', 'recommendation')
likes = pd.read_csv(os.path.join(csv_directory, 'likes.csv'))
users = pd.read_csv(os.path.join(csv_directory, 'users.csv'))
posts = pd.read_csv(os.path.join(csv_directory, 'posts.csv'))

# Merge the data
data = pd.merge(pd.merge(likes, users, on='user_id'), posts, on='post_id')

# Create a user-post rating matrix
user_post_ratings = data.pivot_table(
    index='user_id', columns='post_id', values='like').fillna(0)

# Convert the DataFrame to a sparse matrix with a floating data type
user_post_ratings_sparse = csr_matrix(
    user_post_ratings.values, dtype=np.float32)

# Perform matrix factorization using Singular Value Decomposition (SVD)
k = min(user_post_ratings_sparse.shape) - 1  # Number of latent factors
U, sigma, Vt = svds(user_post_ratings_sparse, k=k)
sigma = np.diag(sigma)

# Predict ratings for unseen posts
all_user_ratings = np.dot(np.dot(U, sigma), Vt)
pred_user_ratings = pd.DataFrame(
    all_user_ratings, columns=user_post_ratings.columns, index=user_post_ratings.index)

# Get the top recommendations for a user


def recommend_posts(user_id, num_recommendations=10):
    user_ratings = pred_user_ratings.loc[user_id].sort_values(ascending=False)
    user_liked_posts = likes.loc[likes['user_id'] == user_id]['post_id']

    recommendations = pd.DataFrame(
        columns=['post_id', 'view_count', 'score'])
    for post_id, rating in user_ratings.items():
        if post_id not in user_liked_posts:
            post = posts.loc[posts['post_id'] == post_id]
            view_count = post['views_count_'].values[0]
            score = rating * view_count
            recommendations = recommendations._append(
                {'post_id': int(post_id), 'view_count': int(view_count), 'score': int(score)}, ignore_index=True)

    recommendations = recommendations.sort_values(
        by='score', ascending=False).head(num_recommendations)
    return recommendations


# Example usage
# user_id = 2
# recommended_posts = recommend_posts(user_id)
# print(recommended_posts)

# export DJANGO_SETTINGS_MODULE=config.settings
