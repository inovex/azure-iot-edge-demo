# Azure IoT Edge Demo

This repo contains a demo Azure IoT Edge application consisting of two python components:

* An [IoT device](/device) to be run on a Raspberry Pi, which reads data from a DS18B20 sensor and sends a message towards the cloud each second.
* An [IoT Edge deployment](/deployment.template.json) with a single [module](/modules/node), which intercepts and prints these messages before forwarding them to the cloud.

The python code is based on Microsoft's [Azure IoT Python samples](https://github.com/Azure-Samples/azure-iot-samples-python).

## Building and Testing the application

The following steps will guide you in setting up the demo application. The setup used in the live demo looked as following:

![Demo setup consisting of two Raspberry Pis used as edge-device-0 and edge-device-1 respectively and an additional Raspberry Pi used as edge-node. They communicate over WiFi, which is linked to the internet, where the IoT Hub called iotedgedemo can be reached.](/img/hardware.png "Hardware setup from Demo")

### General prerequisites

* You'll need an azure subscription with an Azure IoT Hub and a container registry, follow [this quickstart guide from Microsoft](https://docs.microsoft.com/en-us/azure/iot-edge/quickstart-linux) for guidance
* Install the [azure cli with the iotedge extension](https://github.com/Azure/azure-iot-cli-extension) and login using `az login`
* Install iotedgedev using `pip install iotedgedev` (or use the [VSCode extension](https://marketplace.visualstudio.com/items?itemName=vsciot-vscode.azure-iot-edge)) locally

### Edge Node Prerequisites

* Either provision a VM with Ubuntu-16.04 or a Raspberry Pi with Raspbian
  * Install the iot edge [runtime on your Raspberry Pi](https://docs.microsoft.com/en-us/azure/iot-edge/how-to-install-iot-edge-linux-arm) or [your VM](https://docs.microsoft.com/en-us/azure/iot-edge/how-to-install-iot-edge-linux)
  * Configure the IoT edge device with name `edge-node` by following [these steps](https://docs.microsoft.com/en-us/azure/iot-edge/quickstart-linux#register-an-iot-edge-device)
* Set up Certificates for [the Edge Node](https://docs.microsoft.com/en-us/azure/iot-edge/how-to-create-transparent-gateway)

### Edge Node Deployment

If you have everything set up you first need to change the container registry settings in the [module.json](/modules/node/module.json) and [deployment.template.json](/deployment.template.json). Simply replace `inovexedgedemoacr.azurecr.io` with your registry URI and adjust the credentials accordingly.
You can then deploy to the edge node using the iotedgedev cli:

```sh
# Prepare environment variables for iotedgedev, skip this part when redeploying
$HUB_NAME=<your-hub-name>
echo "BUILD_BUILDNUMBER=0.0.1" > .env
echo "IOTHUB_CONNECTION_STRING=$(az iot hub show-connection-string -n $HUB_NAME | jq '.cs')" >> .env
echo "DEVICE_CONNECTION_STRING=$(az iot hub device-identity show-connection-string -n $HUB_NAME -d edge-node | jq '.cs')" >> .env
# Build & Push Docker images and deploy
iotedgedev build -f deployment.template.json -P arm32v7 --push --deploy
```

### Edge Device Prerequisites

* Provision two Raspberry Pis with an DS18B20 sensor and Raspbian as Edge Devices
* The Pis should be able to reach the Edge Node on a static IP
* The IP address of the Edge Node needs to be added to /etc/hosts of the devices: `echo "<Edge Node ip> edge-node" >> /etc/hosts`
* [Install the certificates from the Edge Node on the Edge devices](https://docs.microsoft.com/en-us/azure/iot-edge/how-to-connect-downstream-device)
* Create a device identity in your IoT Hub for both:

```sh
HUB_NAME=<your-hub-name>
for iotdevice in edge-device-1 edge-device-2; do
   az iot hub device-identity create -n $HUB_NAME -d $iotdevice
   echo "Created $iotdevice. Connection String:"
   az iot hub device-identity show-connection-string -n $HUB_NAME -d $iotdevice | jq ".cs"
done
```

Then refer to [the device readme](./device/README.md) to setup the sensor and software.

### Edge Device Deployment

Retrieve the connection strings for your devices if not done already:

```sh
az iot hub device-identity show-connection-string -n $HUB_NAME -d edge-device-0 | jq '.cs'
az iot hub device-identity show-connection-string -n $HUB_NAME -d edge-device-1 | jq '.cs'
```

Then simply copy the device folder on the Pi, install the requirements and run it:

```sh
# copy files to pi TODO replace with git pull?
scp ./device <user>@<your-edge-device-ip>:~/device
ssh <user>@<your-edge-device-ip>
cd device
pip install -r requirements.txt
python device.py sensor '<your-device-connection-string-in-quotes>'
```
