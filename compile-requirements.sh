#!/usr/bin/env bash
set -e -o pipefail

pip-compile --verbose --no-emit-index-url requirements.in
