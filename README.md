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

    - Unset the S3_BUCKET environmental variable <br>
    `unset S3_BUCKET` <br>

    - Add AWS credentials to environment <br>
    `export S3_BUCKET=<name of S3 bucket>` <br>
    `export AWS_ACCESS_KEY_ID=<ID of AWD access key>` <br>
    `export AWS_SECRET_ACCESS_KEY=<AWS secret access key>`

5. Add environmental _FLASK_ variable <br>
`export FLASK_APP=run`

6. Initialize db schema <br>
`flask db init`

7. Load tables <br>
`flask db migrate` 

8. Create database <br>
`flask db upgrade`

9. Create a default admin user. _Read console output_ <br>
`flask seed`

10. Run tests <br>
`flask test`

11. Start server <br>
`flask run`

12. Populate db with dummy data using the provided utility script. <br>

    - If using the local drive as the storage for the images, run <br>
    `python scripts/populate.py --local --images <storage folder>` <br>

    - If using AWS as the storage for the images, simply run (remember to set AWS credentials as shown in step 4) <br>
    `python scripts/populate.py` <br>

Server should be ready now, by default at http://127.0.0.1:5000

### Quick db restart

If it is needed to clear the db and images, and restart the server, run the following

1. Recreate postgres db
`./clear-db.sh; psql postgres -c "CREATE DATABASE oasis"` <br>

2. Delete images (adding the local flag is using local storage)
`python scripts/delete_images.py [--local]` <br>

3. Repopulate the db
`python scripts/populate.py [--local --images <storage folder>]` <br>

4. Restart server <br>
`flask run`

### Heroku installation

The server has been tested on Heroku. General steps involve

1. Create Heroku app <br>
`heroku create server-oasis` <br>

2. Set environment <br>
`heroku addons:create heroku-postgresql:hobby-dev --app server-oasis` <br>
`heroku config:set S3_BUCKET=oasis-storage` <br>
`heroku config:set AWS_ACCESS_KEY_ID=<ID of AWD access key> AWS_SECRET_ACCESS_KEY=<AWS secret access key>` <br>

3. Push changes <br>
`git push heroku` <br>

4. Populate DB and AWS <br>
`python scripts/populate.py` <br>

### Stand-alone WSGI server

The OASIS server can be run as a stand-alone WSGI application using a Python WSGI HTTP Serve like Gunicorn (listed in the requirements):

`gunicorn --bind 127.0.0.1:5000  "run:create_app()"`

### Contributors

* The initial version of the OASIS server was developed by Maxim Tsybanov (oasis@tsybanov.com) during the X-Lab Spark practicum class at Boston University in Summer 2019.
