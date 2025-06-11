#!/bin/bash

# define current environment
SCRIPT=$(realpath "$0")
SCRIPT_PATH=$(dirname "$SCRIPT")
RENDERER_PATH=$(realpath "$SCRIPT_PATH/../renderer")
EXECUTABLE_PATH=$(realpath "$RENDERER_PATH/linux-aarch64/renderer")

# generate preview file and save it to
xvfb-run "$EXECUTABLE_PATH" "$@"

