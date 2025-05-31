#!/bin/bash

# define current environment
SCRIPT=$(realpath "$0")
SCRIPT_PATH=$(dirname "$SCRIPT")
PROCESSING_PATH=$(realpath "$SCRIPT_PATH/../../processing-4.3.4/processing-java")
RENDERER_PATH=$(realpath "$SCRIPT_PATH/../renderer")

# generate preview file and save it to
xvfb-run "$PROCESSING_PATH" --sketch="$RENDERER_PATH" --run "$@"
