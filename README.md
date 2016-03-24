# TwitterRepManagement
This is my final year project - the Twitter Reputation Monitor, it is a Django web application that allows you to monitor online reputation of companies over Twitter.

Video Demo: 

https://www.youtube.com/watch?v=rOkPjH_x3u4

PowerPoint Presentation: 

https://docs.google.com/presentation/d/1MiGlGt3kaF868Dty4-q3hPsEGrxciItwIFvnjf8M8rc/edit#slide=id.p4

To set up the system, first clone the whole repo into your local machine:
```
git clone git@github.com:vincentfung13/TwitterRepManagement.git
```

## Installing the Dependencies

Then navigate to the TwitterRepManagemnet directory and install the requirements with pip:
```
pip install -r requirements.txt
```

This system has a dependency of [PostgreSQL] (http://www.postgresql.org/download/) version 9.2 onwards and Django 1.9 onwards. You will also need to install PostgreSQL's python driver [here] (http://initd.org/psycopg/docs/install.html).

## Setting up the project

First create a database called TwitterRepMonitor in postgres, you can do this via command line:
```
createdb TwitterRepMonitor
```

Then you should open TwitterRepManagement/TwitterRepManagement/settings.py, in the python dictionary called DATABASES, change field "USER" and "PASSWORD" to yours (you can also change the host and port if you need to).

Now you can use the provided scripts to set up the project, under the root TwitterRepManagement directory:
```
<!-- This will do a migration to your database and populate the traning set table -->
sh setup.sh

<!-- This starts the application and set up a cron job for the reputation monitor -->
sh start_app.sh
```

After this step you can visit the application site on your localhost. If you want to turn on the tweet streaming, you can simply run:
```
python manage.py start_streamer
```

Note that the reputation monitor will run once a day, you might want to delete the cron job. After you shut down the server, a file will be opened in which there is a list of your crontabs, to delete the reputation monitor run, simply remove the line "0 0 */1 * * monitor_setup.sh" and save it.



