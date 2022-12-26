#!/bin/bash
NAME="puzzlee"
DJANGODIR="/usr/local/src/puzzlee/"
VENVDIR="${DJANGODIR}/.venv"
SOCKFILE="/usr/local/src/puzzlee/run/gunicorn.sock"
USER=puzzlee_user
GROUP=webapps
NUM_WORKERS=3
TIMEOUT=120
DJANGO_SETTINGS_MODULE=config.settings.production
DJANGO_WSGI_MODULE=config.wsgi

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source $VENVDIR/bin/activate

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start you Django Unicorn 
# Programs meant to be run under supervisor should not
# daemonize themselves.
# (do not use --daemon)

exec $VENVDIR/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
    --name $NAME \
    --workers $NUM_WORKERS \
    --timeout $TIMEOUT \
    --user=$USER --group=$GROUP \
    --bind 127.0.0.1:8000 \
    --log-level=warning \
    --log-file=-

