Please, read documentation in _docs_ folder.

### Installing:

1. Install npm modules <br>
`npm install --prefix src/frontend`

2. Create a new webpack bundle <br>
`npm run build --prefix src/frontend`

3. Install python libraries used by Flask <br>
`pip install -r requirements.txt`

4. Add environmental _FLASK_ variable <br>
`export FLASK_APP=run`

5. Initialize db schema <br>
`flask db init`

6. Load tables <br>
`flask db migrate` 

7. Create database <br>
`flask db upgrade`

8. Create a default admin user. _Read console output_ <br>
`flask seed`

9. Run tests <br>
`flask test`

10. Start server <br>
`flask run`

### Starting:
1. Add environmental _FLASK_ variable <br>
`export FLASK_APP=run`

2. Start server <br>
`flask run`
