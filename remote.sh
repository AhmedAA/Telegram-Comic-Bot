#!/bin/bash

CONTAINER="mjaaabot"

RUNNING=$(docker inspect --format="{{ .State.Running }}" $CONTAINER 2> /dev/null)

if [ $RUNNING == "false" ]; then
  docker restart mjaaabot
fi

#Add following to crontab -e
#*/3 * * * * ./remote.sh
#*/15 * * * * docker restart mjaaabot

