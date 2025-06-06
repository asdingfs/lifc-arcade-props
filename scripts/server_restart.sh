#!/bin/bash

sudo systemctl restart pixel_pusher_server.service && \
  sudo systemctl restart gunicorn_server.service