#!/bin/bash
python manage.py populate_training_set

printf "INFO: Applying migrations."
python manage.py makemigrations
python manage.py migrate

printf "INFO: Set up successfully."
