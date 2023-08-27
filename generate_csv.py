
# autopep8: off
import os
import sys
from pathlib import Path
import pandas as pd

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "socialapi.settings")

# Add the path to your Django project directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import and configure Django
import django
from django.conf import settings
django.setup()

# Now you can import your models
from posts.models import Post
from users.models import CustomUser
from django.db.models import F
from django.contrib.auth import get_user_model

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
User =get_user_model()

# autopep8: on


def generate_csv():
    logger.info("Generating CSV files...")
    csv_directory = os.path.join(settings.BASE_DIR, 'api', 'recommendation')

    # Generate CSV for users
    users_data = CustomUser.objects.values(
        user_id=F('id'), username_=F('username'))
    users_df = pd.DataFrame(users_data)
    users_df.to_csv(os.path.join(csv_directory, 'users.csv'), index=False)

    # Generate CSV for posts
    posts_data = Post.objects.values(
        post_id=F('id'), views_count_=F('views_count'))
    posts_df = pd.DataFrame(posts_data)
    posts_df.to_csv(os.path.join(csv_directory, 'posts.csv'), index=False)

    # Generate likes data
    likes_data = []
    for user in User.objects.all():
        for post in Post.objects.all():
            like_status = 1 if user in post.likes.all() else 0
            likes_data.append({
                'user_id': user.id,
                'post_id': post.id,
                'like': like_status
            })

    # Create a DataFrame from the data
    likes_df = pd.DataFrame(likes_data)

    # Save the DataFrame to a CSV file
    likes_csv_file = os.path.join(csv_directory, 'likes.csv')
    likes_df.to_csv(likes_csv_file, index=False)


if __name__ == "__main__":
    generate_csv()
