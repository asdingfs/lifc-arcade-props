#!/bin/bash

# define current environment
SCRIPT=$(realpath "$0")
SCRIPT_PATH=$(dirname "$SCRIPT")
RENDERER_PATH=$(realpath "$SCRIPT_PATH/../renderer")

# generate preview file and save it to
processing-java --sketch="$RENDERER_PATH" --run "$@"