#!/usr/bin/env bash
# Smoke test: ask the live API one known question and check the answer.
set -euo pipefail

API_URL="${1:?Usage: smoke_test.sh API_URL}"
BODY_FILE="$(mktemp)"

echo "Smoke test against ${API_URL}/calculate"

STATUS=$(curl -s -o "$BODY_FILE" -w "%{http_code}" \
  -X POST "${API_URL}/calculate" \
  -H "Content-Type: application/json" \
  -d '{"server_type":"t3.micro","hours":730,"db_type":"none","db_hours":0,"nat":"no","gb_stored":10,"gb_out":50}')

echo "HTTP status: ${STATUS}"
echo "Body: $(cat "$BODY_FILE")"

if [ "$STATUS" != "200" ]; then
  echo "FAIL: expected HTTP 200"
  exit 1
fi

if ! grep -q '"total": 8.85' "$BODY_FILE"; then
  echo "FAIL: expected total 8.85 (t3.micro for a month + 10 GB in S3)"
  exit 1
fi

echo "PASS"