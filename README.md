## OASIS server

This is the server backend of the OASIS platform. Please, read REST API reference in _docs_ folder, and general documentation in the _wiki_.

### Installing:

1. Install python libraries used by Flask <br>
`pip install -r requirements.txt`

2. Add environmental _DATABASE_URL_ variable <br>
`export DATABASE_URL=postgresql://localhost/oasis`

3. Add AWS credentials to environment <br>
`export S3_BUCKET=<name of S3 bucket>` <br>
`export AWS_ACCESS_KEY_ID=<ID of AWD access key>` <br>
`export AWS_SECRET_ACCESS_KEY=<AWS secret access key>`

4. Add environmental _FLASK_ variable <br>
`export FLASK_APP=run`

5. Create PostgreSQL database <br>
`psql postgres -c "CREATE DATABASE oasis"`

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

To clear the existing database before re-install the server, run the following script:

`./clear-db.sh`

### Starting:

1. Add environmental _FLASK_ variable <br>
`export FLASK_APP=run`

2. Add environmental _DATABASE_URL_ variable <br>
`export DATABASE_URL=postgresql://localhost/oasis`

3. Start server <br>
`flask run`

### Stand-alone WSGI server

The OASIS server can be run as a stand-alone WSGI application using a Python WSGI HTTP Serve like Gunicorn (listed in the requirements):

`gunicorn --bind 127.0.0.1:5000  "run:create_app()"`

### Populating the database

Look into the scripts subfolder for instructions and scripts on how to populate the database with dummy data for testing.

### Contributors

* The initial version of the OASIS server was developed by Maxim Tsybanov (oasis@tsybanov.com) during the X-Lab Spark practicum class at Boston University in Summer 2019.
