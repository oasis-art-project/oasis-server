#!/bin/bash

export FLASK_APP=run
flask db init
flask db migrate
flask db upgrade
flask seed