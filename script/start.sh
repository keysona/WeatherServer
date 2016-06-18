#!/bin/bash

SCRIPT_DIR=$(dirname ${0})
PROJECT_DIR=$(dirname ${SCRIPT_DIR})

source $SCRIPT_DIR/env.sh
workon weather-server

# cd ..

nohup \
gunicorn -w 4 -b 127.0.0.1:5000 \
--error-logfile /var/log/error-weather-server.log \
--access-logfile /var/log/access-weather-server.log \
manage:app 1>/dev/null 2>&1 \
&
