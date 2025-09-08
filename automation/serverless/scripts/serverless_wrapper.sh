#!/bin/bash

# Serverless Automation Wrapper
# Quick access to serverless commands from automation directory

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/serverless"

# Pass all arguments to the run script
./run.sh "$@"
