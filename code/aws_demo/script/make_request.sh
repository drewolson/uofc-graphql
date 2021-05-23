#!/usr/bin/env bash

curl \
  -H 'content-type: application/json' \
  -X POST \
  -d '{"query": "{ randomNumber dayOfTheWeek }"}' \
  https://ehde0ewced.execute-api.us-east-2.amazonaws.com/graphql
