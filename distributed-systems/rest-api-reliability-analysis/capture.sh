#!/usr/bin/env bash
set -euo pipefail

URL="https://cloudroom-unreliablebanking-747241312189.europe-west1.run.app/getbalance"
OUT="responses.csv"

echo -n "" > "$OUT"


for i in $(seq 1 120); do
  ts=$(date "+%Y-%m-%d %H:%M:%S")
  code=$(curl -s -o /dev/null -w "%{http_code}" "$URL" || echo "000")
  echo "$ts, $code" >> "$OUT"
  sleep 1
done

echo "Done. Wrote $(wc -l < "$OUT") lines to $OUT"
