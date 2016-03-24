printf "INFO: Starting a cron job for reputation monitor."
crontab -l > mycron
echo "0 0 */1 * * monitor_setup.sh" > mycron
crontab mycron
rm mycron

printf "INFO: Starting the server on local host."
python manage.py runserver

crontab -e


