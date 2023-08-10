#!/bin/sh
rm db.*
rm */migrations/ -r
rm media/ -r 
python3 manage.py makemigrations users market
python3 manage.py migrate
python3 manage.py collectstatic
python3 manage.py shell < f_seeder.py