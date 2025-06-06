#!/bin/bash

sudo tail -f /var/log/nginx/access.log /var/log/nginx/error.log \
  /var/log/gunicorn/access.log /var/log/gunicorn/error.log
