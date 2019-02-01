#!/bin/bash
HUB_NAME=$1
az iot hub device-identity create -n $HUB_NAME -d edge-node --edge-enabled
az iot hub device-identity show-connection-string -n $HUB_NAME -d edge-node | jq ".cs"