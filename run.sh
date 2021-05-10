#!/bin/bash

#gunicorn --bind 127.0.0.1:5000 --worker-class eventlet -w 1 "run:create_app()"
gunicorn --bind 127.0.0.1:5000 "run:create_app()"
