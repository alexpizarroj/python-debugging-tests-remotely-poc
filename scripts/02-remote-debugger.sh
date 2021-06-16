#!/usr/bin/env bash
set -e -o pipefail

docker run \
    -it --rm \
    --mount type=bind,source="$(pwd)",target=/app \
    --publish 7200:7200 \
    python-remote-debugging-poc \
    pytest --pdb --pdbcls=remote_dbg:RemotePdb tests/
