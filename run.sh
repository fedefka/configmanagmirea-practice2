#!/bin/sh
set -eu
project_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python_cmd=python3
if [ -x "$project_dir/.venv/bin/python" ]; then
    python_cmd="$project_dir/.venv/bin/python"
fi
exec "$python_cmd" "$project_dir/src/main.py" "$@"
