# Azure IoT Edge Demo

This repo contains a demo Azure IoT Edge application consisting of two python components:

* An [IoT device](/device) to be run on a Raspberry Pi, which reads data from a DS18B20 sensor and sends a message towards the cloud each second.
* An [IoT Edge deployment](/deployment.template.json) with a single [module](/modules/node), which intercepts and prints these messages before forwarding them to the cloud.

The python code is based on Microsoft's [Azure IoT Python samples](https://github.com/Azure-Samples/azure-iot-samples-python).

## Building and Testing the application

The following steps will guide you in setting up the demo application

### Prerequisites

* You'll need an azure subscription with an Azure IoT Hub and a container registry, follow [this quickstart guide from Microsoft](https://docs.microsoft.com/en-us/azure/iot-edge/quickstart-linux) for guidance
* Install the [azure cli with the iotedge extension](https://github.com/Azure/azure-iot-cli-extension) and login using `az login`
* An VM (or Physical device, we used a Raspberry Pi) as Edge Node and two Raspberry Pis with an DS18B20 sensor each as Edge Devices (the Pis can also be simulated with the included Dockerfile).
* Set up Certificates for [the Edge Node](https://docs.microsoft.com/en-us/azure/iot-edge/how-to-create-transparent-gateway) and [install them on the Edge devices](https://docs.microsoft.com/en-us/azure/iot-edge/how-to-connect-downstream-device)
* Install iotedgedev using `pip install iotedgedev` (or use the [VSCode extension](https://marketplace.visualstudio.com/items?itemName=vsciot-vscode.azure-iot-edge))

### Deploying to the edge node

If you have everything set up you first need to change the container registry in