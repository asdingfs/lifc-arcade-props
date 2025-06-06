#!/bin/bash

sudo mkdir -p /var/log/nginx /var/log/gunicorn
sudo tail -f /var/log/nginx/access.log /var/log/nginx/error.log \
  /var/log/gunicorn/access.log /var/log/gunicorn/error.log