## OASIS server

This is the server backend of the OASIS platform. Please, read REST API reference in _docs_ folder, and general documentation in the _wiki_.

### Installing:

1. Install python libraries used by Flask <br>
`pip install -r requirements.txt`

2. Add environmental _FLASK_ variable <br>
`export FLASK_APP=run`

3. Initialize db schema <br>
`flask db init`

4. Load tables <br>
`flask db migrate` 

5. Create database <br>
`flask db upgrade`

6. Create a default admin user. _Read console output_ <br>
`flask seed`

7. Run tests <br>
`flask test`

8. Start server <br>
`flask run`

### Starting:
1. Add environmental _FLASK_ variable <br>
`export FLASK_APP=run`

2. Start server <br>
`flask run`

### Contributors

* The initial version of the OASIS server was developed by Maxim Tsybanov (oasis@tsybanov.com) during the X-Lab Spark practicum class at Boston University in Summer 2019.
