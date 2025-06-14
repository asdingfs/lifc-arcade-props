#!/bin/bash

sudo tail -f /var/log/nginx/access.log /var/log/nginx/error.log \
  /var/log/gunicorn/access.log /var/log/gunicorn/error.log \
  /var/log/redis/redis-server.log \
  /home/server/lifc-arcade-props/scripts/processing-java.log

