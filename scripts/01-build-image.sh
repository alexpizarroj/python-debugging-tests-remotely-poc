#!/usr/bin/env bash
set -e -o pipefail

DOCKER_SCAN_SUGGEST=false docker build -t "python-remote-debugging-poc" .
