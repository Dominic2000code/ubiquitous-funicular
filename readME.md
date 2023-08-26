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
