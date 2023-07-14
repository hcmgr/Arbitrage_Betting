#!/bin/bash

# Set default value for log
log=false

# Check if --log parameter is provided and set log accordingly
if [[ "$@" == *"--log=True"* ]]; then
    log=true
fi

# Execute arb_finder.py with or without output redirection based on log value
if [ "$log" = true ]; then
    python3 src/server/arb_finder.py > src/server/utils/run.txt
else
    python3 src/server/arb_finder.py
fi
