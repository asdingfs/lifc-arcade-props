#!/bin/bash

SCRIPT=$(realpath "$0")
SCRIPT_PATH=$(dirname "$SCRIPT")

# check if script is already running, if yes, kill it
script_name=processing-java
for pid in $(pgrep -x "$script_name"); do
    if [ $pid != $$ ]; then
        kill -9 $pid
    fi
done

# and start a new one
processing-java --sketch="$(realpath "$SCRIPT_PATH/../renderer")" --run "$@"