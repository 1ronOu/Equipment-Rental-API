#!/usr/bin/env bash

set -e

echo "run mig"

alembic upgrade head
echo "all good"

exec "$@"