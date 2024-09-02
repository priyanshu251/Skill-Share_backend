#!/bin/bash

rm db.sqlite3
source venv/bin/activate
python manage.py migrate
python manage.py loaddata backup.json
python manage.py runserver