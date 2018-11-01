#How to Contribute

0. Create virtual environment with python v3.6 (https://virtualenv.pypa.io/en/latest/)

1. clone this repositories
2. create database
3. make file `.env` in project root based on `.env.tmp` and specify settings. See https://github.com/joke2k/django-environ for configure database
4. install requirements: `pip install -r requirements.txt`
5. run migration `python manage.py migrate`
6. create admin user `python manage.py createsuperuser`
7. run dev server