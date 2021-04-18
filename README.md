## OASIS server

This is the server backend of the OASIS platform. Please, read REST API reference in _docs_ folder, and general documentation in the _wiki_.

### Local installation

The server can be run locally with the following steps:

1. Install python libraries used by Flask <br>
`pip install -r requirements.txt`

2. Add environmental _DATABASE_URL_ variable <br>
`export DATABASE_URL=postgresql://localhost/oasis`

3. Create PostgreSQL database <br>
`psql postgres -c "CREATE DATABASE oasis"`

4. Image data can be stored locally as well, or in AWS S3 bucket <br>

    - Add the location of the image upload folder AND unset the S3_BUCKET environmental variable if previously set <br>
    `unset S3_BUCKET` <br>
    `export IMAGE_UPLOAD_FOLDER=<path to local image storage folder>` <br>

    - Add AWS credentials to environment <br>
    `export S3_BUCKET=<name of S3 bucket>` <br>
    `export AWS_ACCESS_KEY_ID=<ID of AWD access key>` <br>
    `export AWS_SECRET_ACCESS_KEY=<AWS secret access key>`

5. Export he environmental variables for email and SMS support:

    - Sendmail configuration: <br>
    `export MAIL_USERNAME=info@oooasis.art` <br>
    `export MAIL_DEFAULT_SENDER=info@oooasis.art` <br>
    `export MAIL_PASSWORD=<email password>` <br>

    - Twilio (SMS) configuration: <br>
    `export TWILIO_ACCOUNT_SID=<Twilio account SID>` <br>
    `export TWILIO_AUTH_TOKEN=<Twilio authorization token>` <br>
    `export TWILIO_PHONE_NUMBER=+14012058293`

6. Add environmental _FLASK_ variable <br>
`export FLASK_APP=run`

7. Initialize db schema <br>
`flask db init`

8. Load tables <br>
`flask db migrate` 

9. Create database <br>
`flask db upgrade`

10. Create a default admin user. _Read console output_ <br>
`flask seed`

11. Run tests <br>
`flask test`

12. Start server <br>
`flask run`

13. Server should be ready now, by default at http://127.0.0.1:5000

14. Populate db with dummy data using the provided utility script <br>

`python scripts/populate.py` <br>
`python scripts/populate.py -url <server URL>` <br>

### Quick db restart

If it is needed to clear the db and images, and restart the server, run the following

1. Recreate postgres db

`./clear-db.sh; psql postgres -c "CREATE DATABASE oasis"` <br>

2. Delete images (adding the local flag is using local storage)

`python scripts/delete_images.py [--local]` <br>

3. Repopulate the db

`python scripts/populate.py -url <server URL>` <br>

4. Restart server <br>
`flask run`

### Heroku installation

The server has been tested on Heroku. General steps involve the following

1. Create Heroku app <br>
`heroku create server-oasis` <br>

2. Set environment <br>
`heroku addons:create heroku-postgresql:hobby-dev --app server-oasis` <br>
`heroku config:set S3_BUCKET=oasis-storage` <br>
`heroku config:set AWS_ACCESS_KEY_ID=<ID of AWD access key> AWS_SECRET_ACCESS_KEY=<AWS secret access key>` <br>
`heroku config:set MAIL_USERNAME=info@oooasis.art MAIL_DEFAULT_SENDER=info@oooasis.art MAIL_PASSWORD=<email password>` <br>
`heroku config:set TWILIO_ACCOUNT_SID=A<Twilio account SID> TWILIO_AUTH_TOKEN=<Twilio authorization token> TWILIO_PHONE_NUMBER=+14012058293` <br>

3. Push changes <br>
`git push heroku` <br>

4. Populate DB and AWS <br>
`python scripts/populate.py` <br>

For more information, check the [wiki entry](https://github.com/codeanticode/oasis-server/wiki/Server-deployment).

### Stand-alone WSGI server

The OASIS server can be run as a stand-alone WSGI application using a Python WSGI HTTP Serve like Gunicorn (listed in the requirements):

`gunicorn --bind 127.0.0.1:5000  "run:create_app()"`

### Contributors

* The initial version of the OASIS server was developed by Maxim Tsybanov (oasis@tsybanov.com) during the X-Lab Spark practicum class at Boston University in Summer 2019.
