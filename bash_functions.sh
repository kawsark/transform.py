#!/bin/bash

# Some utility functions to easily encode and decode invidual fields
az_encode() {
  # Remove prefix
  v=$(echo $1 | awk -F ':' '{print $NF}')
  s=$(vault write -format=json transform/encode/local value=$v transformation=azure) 2>/dev/null
  echo $s | jq -r .data.encoded_value
}

az_decode(){
  # Remove prefix
  v=$(echo $1 | awk -F ':' '{print $NF}')
  s=$(vault write -format=json transform/decode/local value=$v transformation=azure) 2>/dev/null
  echo $s | jq -r .data.decoded_value
}
