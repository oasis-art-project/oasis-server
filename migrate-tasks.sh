#!/bin/bash

export COMMIT_TEXT="added active column to places table"

export FLASK_APP=run
flask db init
flask db migrate -m "${COMMIT_TEXT}" 
flask db upgrade