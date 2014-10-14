#!/usr/bin/env bash
ab -n 1 -c 1 -p data/data.json -T application/json -H "x-api-key: analytics" https://localhost:8887/analytics/report
