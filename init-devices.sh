#!/bin/bash
HUB_NAME=$1
for iotdevice in edge-device-1 edge-device-2; do
   az iot hub device-identity create -n $HUB_NAME -d $iotdevice
   echo "Created $iotdevice. Connection String:"
   az iot hub device-identity show-connection-string -n $HUB_NAME -d $iotdevice | jq ".cs"
done