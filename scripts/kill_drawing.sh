#!/bin/bash

# define current environment
SCRIPT=$(realpath "$0")

# define lockfile arguments
LOCKFILE="/tmp/lifc-arcade-props.lock"

# This function finds all child processes of a given PID recursively
pids=()
get_nested_pids() {
    pids+=("$1")
    local parent_pid=$1
    local child_pids=($(pgrep -P "$parent_pid"))
    for child in "${child_pids[@]}"; do
        get_nested_pids "$child"
    done
}

# Check if lockfile exists
if [ -f "$LOCKFILE" ]; then
  LOCK_PID=$(cat "$LOCKFILE")
  get_nested_pids $LOCK_PID

  for pid in "${pids[@]}"; do
    if ps -p "$pid" > /dev/null 2>&1; then # if process still running
      # attempt to send SIGTERM to the process
      kill -TERM "$pid"
    fi # else, don't do anything
  done
fi
rm -f "$LOCKFILE"