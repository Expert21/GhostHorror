#!/bin/bash
# Ghost Horror Mode Launcher

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check for virtual environment
if [ ! -d "venv" ]; then
    echo "Setting up virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install pygame python-xlib
else
    source venv/bin/activate
fi

# Run Ghost Horror Mode
python -m ghost_horror.main "$@"

