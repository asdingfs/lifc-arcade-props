#!/bin/bash

sudo systemctl daemon-reload
sudo systemctl restart redis
sudo systemctl restart pixel_pusher_server.service
sudo systemctl restart gunicorn_server.service
