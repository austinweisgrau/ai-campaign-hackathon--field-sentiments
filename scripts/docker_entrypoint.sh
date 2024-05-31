#!/bin/bash

# Entrypoint for running webserver and flask in both production and local env
# Uses gunicorn to run flask process

set -e

/usr/local/bin/gunicorn -b 0.0.0.0:3000 --workers 4 wsgi:app --access-logfile '-' --timeout 1080
