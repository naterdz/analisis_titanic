#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
git add .
git commit -m "${1:-Actualiza y limpieza proyecto Titanic}"
git push
