#!/bin/bash

sudo mkdir -p /var/log/inputs
sudo tail -f /var/log/inputs/readers.log /var/log/inputs/buttons.log