#!/bin/bash
printf "INFO: Applying migrations."
python manage.py makemigrations
python manage.py migrate

python manage.py populate_training_set
printf "INFO: Set up successfully."
