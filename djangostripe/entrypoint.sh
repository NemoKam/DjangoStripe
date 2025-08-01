#! /usr/bin/env bash

sleep 5 && ./prepare_db.sh && gunicorn djangostripe.wsgi:application --bind 0.0.0.0:8000 --workers=4 --timeout 900
