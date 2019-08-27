## OASIS server

This is the server backend of the OASIS platform. Please, read REST API reference in _docs_ folder, and general documentation in the _wiki_.

### Installing:

1. Install python libraries used by Flask <br>
`pip install -r requirements.txt`

2. Add environmental _FLASK_ variable <br>
`export FLASK_APP=run`

3. Add environmental _DATABASE_URL_ variable <br>
`export DATABASE_URL=postgresql://localhost/oasis`

4. Initialize db schema <br>
`flask db init`

5. Load tables <br>
`flask db migrate` 

6. Create database <br>
`flask db upgrade`

7. Create a default admin user. _Read console output_ <br>
`flask seed`

8. Run tests <br>
`flask test`

9. Start server <br>
`flask run`

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

### Contributors

* The initial version of the OASIS server was developed by Maxim Tsybanov (oasis@tsybanov.com) during the X-Lab Spark practicum class at Boston University in Summer 2019.
