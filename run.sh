#!/bin/bash

gunicorn --bind 127.0.0.1:5000 "run:create_app()"
