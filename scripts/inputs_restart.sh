#!/bin/bash

sudo systemctl daemon-reload
sudo systemctl restart player_1_rfid.service
sudo systemctl restart player_2_rfid.service
sudo systemctl restart start_button.service
sudo systemctl restart reset_button.service