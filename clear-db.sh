#!/bin/bash

psql postgres -c "DROP DATABASE oasis"
rm -Rf migrations