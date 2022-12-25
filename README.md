## OASIS server

This is the server backend of the OASIS platform. Please, read REST API reference in _docs_ folder, and general documentation in the _wiki_.

### Local installation

The server can be run locally with the following steps:

1. A few preliminary checks (usually only need to do once):
    * Make sure postgres server is running locally (you can download the official tools for macOS, Windows, and Linux from [here](https://www.postgresql.org/)).
    * It is recommended to create a virtual environment for the server so specific packages requirements do not conflict with the system-wide install or other environments that might be in use. For example if you call this environment ```oasis-server-env```, then the steps for creating it and installing the packages would be: <br>
    `python -m venv oasis-server-env` <br>
    `source oasis-server-env/bin/activate` <br>
    `pip install -r requirements.txt` <br>

2. Setup environmental variable pointing to the location where the images shuld be stored. Since we are running locally, including the [OASIS webapp](https://github.com/oasis-art-project/oasis-webapp/), then the image folder should be inside the webapp's public folder and named `dev-images`. So if the webapp is installed at `~/oasis-webapp`, then we would do (starting with the unset to make sure that the local server does not try to use an S3 bucket to store images): <br>
`unset S3_BUCKET` <br>
`export IMAGE_UPLOAD_FOLDER=~/oasis-webapp/public/dev-images/` <br>
`rm -Rf $IMAGE_UPLOAD_FOLDER` <br>

3. Export the environmental variables required by the server.

    - First group of variables contain the admin credentials, flask app to run, and URL of the webapp: <br>
    `export ADMIN_EMAIL=admin@youroasis.art` <br>
    `export ADMIN_PASSWORD=your_admin_password` <br>
    `export DATABASE_URL=postgresql://localhost/oasis` <br>
    `export FLASK_APP=run` <br>
    `export WEBAPP_URL=http://localhost:3000/` <br>

    - Second group of variables contain sendmail configuration (the server sends emails to users when there are new notifications, as well as a notification to a predefined inbox when a new user fills out the registration form): <br>
    `export MAIL_USERNAME=info@youroasis.art` <br>
    `export MAIL_DEFAULT_SENDER=info@youroasis.art` <br>
    `export MAIL_NEW_USER_INBOX=register@youroasis.art` <br>
    `export MAIL_PASSWORD=your_mail_password` <br>
    `export MAIL_SERVER=mail.server.com` <br>
    `export MAIL_PORT=587` <br>

5. Recreate the postgres database: <br>
`./clear-db.sh; psql postgres -c "CREATE DATABASE oasis"`

6. Initialize db schema, load tables, updgrade db, creates the admin user (using the values set in the step before): <br>
`flask db init; flask db migrate; flask db upgrade; flask seed` <br>

7. If all the previous steps run without errors, you are ready to launch the local server. This can be done in differnt ways.
    
    - Using Flask's development server, which does not support WebSocket (OASIS has a built-in chat system that requires WebSocket, so that would not work with this server): <br>
    `flask run` <br>

    - Using [gunicorn] webserver, which supports WebSocket. There are two possible launch commands, currently only the second one works due to [this issue](https://github.com/oasis-art-project/oasis-server/issues/102). <br>
    `gunicorn --bind 127.0.0.1:5000 --worker-class eventlet -w 1 "run:create_app()"` <br>
    `gunicorn --bind 127.0.0.1:5000 -k gevent "run:create_app()"`

8. Server should be ready now, by default at http://127.0.0.1:5000

9. You can populate the OASIS db with demo data provided in [this repo](https://github.com/oasis-art-project/demo-data) using one of the convenience scripts in the ```scripts``` folder. If you clone the demo-data repo to some location in your computer, for example ```~/demo-data``` then you could run (from the root of the server folder): <br>
`python scripts/populate.py -u http://127.0.0.1:5000 -f ~/demo-data -d` <br>

10. Once the local server is running and the database has been initialized with some data, you can install and run the [OASIS webapp](https://github.com/oasis-art-project/oasis-webapp/) locally.

### Installation on Heroku and AWS

The OASIS server can be installed on Heroku, with an AWS S3 bucket to store images. Once your Heroku and AWS accounts are ready, the deployment of the sever can be performed with the following steps (where we assume the Heroku app is called ```my-oasis-server```, the S3 bucket is ```my-oasis-storage```, and we install it on the ```prod``` remote):

1. Delete previous data and destroy server (optional) to start from scratch: <br>
`python scripts/delete_all.py -u https://my-oasis-server.herokuapp.com/ -e <admin email> -p <admin password>` <br>
`heroku apps:destroy my-oasis-server --confirm=my-oasis-server`

2. Create server: <br>
`heroku create my-oasis-server --remote prod` <br>

3. Create database: <br>
`heroku addons:create heroku-postgresql:mini --app my-oasis-server` <br>

4. Set S3 bucket: <br>
```heroku config:set S3_BUCKET=my-oasis-storage` --remote prod```

5. Set environmental variables: <br>
`heroku config:set WEBAPP_URL=https://myoasis.art/ --remote prod` <br>
`heroku config:set ADMIN_EMAIL=<admin email> ADMIN_PASSWORD=<admin password> --remote prod` <br>
`heroku config:set AWS_ACCESS_KEY_ID=<access key> AWS_SECRET_ACCESS_KEY=<secret access key> --remote prod` <br>
`heroku config:set MAIL_USERNAME=<mail username> MAIL_DEFAULT_SENDER=<outbox address> MAIL_NEW_USER_INBOX=<new user inbox> MAIL_PASSWORD=<mail password> MAIL_SERVER=<mail server> MAIL_PORT=<mail port> --remote prod` <br>

6. Push code in server's main branch to Heroku' main branch: <br>
`git push staging main:main` <br>

7. If all the previous steps were succesful, then the server db can be initialized with some data: <br>
`python scripts/populate.py -u https://my-oasis-server.herokuapp.com/ -f <data folder>` <br>

### Contributors

* The initial version of the OASIS server was developed by Maxim Tsybanov (oasis@tsybanov.com) during the X-Lab Spark practicum class at Boston University in Summer 2019.
