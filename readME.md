# Getting Started

python version 3.11.0

```bash
git clone https://github.com/Dominic2000code/ubiquitous-funicular.git

cd ubiquitous-funicular

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver
```

## Start Redis server

```bash
redis-server
```

## Recommendations

**How the recommendation works**:
    The recommendation system uses collaborative filtering with matrix factorization to predict user preferences for posts. It then generates recommendations based on these predictions, considering factors such as predicted ratings and view counts. Users likes and view counts are used to calculate a recommendation score for each post. The system ultimately suggests posts that users have not yet liked, ranked by their recommendation score.
source: [Link to medium article](https://medium.com/@apokolipsu/building-recommendation-algorithms-for-social-media-platforms-1033de5515d0)

To generate datasets for the recommender you must make sure there is enough data on  different posts(likes and views), then run

```bash
python generate_csv.py # to generate datasets for recommender
```

## Run tests

```bash
Test entire project
python manage.py test

Test by app
python manage.py test <app_name>
```

The site will be available at: <http://127.0.0.1:8000/>

Admin page available at: <http://127.0.0.1:8000/admin>

Documentation available at: <http://127.0.0.1:8000/documentation>
