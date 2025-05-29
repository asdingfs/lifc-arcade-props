#!/bin/bash

# define current environment
SCRIPT=$(realpath "$0")
SCRIPT_PATH=$(dirname "$SCRIPT")
RENDERER_PATH=$(realpath "$SCRIPT_PATH/../renderer")

# define lockfile arguments
LOCKFILE="/tmp/lifc-arcade-props.lock"

# replace currently running drawing process
bash kill_drawing.sh
processing-java --sketch="$RENDERER_PATH" --run "$@" & MY_PID=$!
echo "$MY_PID" > "$LOCKFILE"
