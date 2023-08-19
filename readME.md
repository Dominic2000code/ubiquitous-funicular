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
