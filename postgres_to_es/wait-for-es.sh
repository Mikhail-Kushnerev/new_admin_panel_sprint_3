#!/bin/bash

set -e

host=$ELASTIC_HOST
port=$ELASTIC_PORT
cmd="$@"

>&2 echo "!!!!!!!! Check $host for available !!!!!!!!"

until curl http://"$host":"$port"; do
  >&2 echo "$host is unavailable - sleeping"
  sleep 1
done

>&2 echo "$host is up - executing command"

exec $cmd