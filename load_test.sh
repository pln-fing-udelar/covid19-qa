#!/usr/bin/env bash

set -ex

url=http://localhost:8000

for i in {1..10}; do
  # Different questions so they are cache-missed.
  curl -sS --data "question=¿Qué dijo $i?" -X POST "${url}/question/" -H "accept: application/json" > /dev/null &
done

wait
