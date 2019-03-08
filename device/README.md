# Azure IoT Edge Demo Device

This directory contains code for using an Raspberry Pi as Azure IoT device that reads a temperature sensor and sends its measurements to the Edge Node.

## Getting started

This requires the [Edge Device Prerequisites in this repo's readme](../README.md) to be completed.

### Prerequisites

Set up the sensor following [this tutorial](http://www.circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial/). The steps for connecting the LCD display can be ignored.

Then install some dependencies:

```sh
# Install nodejs
curl -sL http://deb.nodesource.com/setup_8.x | sudo -E bash && sudo apt-get install -y nodejs
# Activate pins for sensor and reboot
sudo $(echo "dtoverlay=w1–gpio" >> /boot/config.txt)
sudo reboot
```

Finally you can run the example by checking out this repository, installing the nodejs dependencies and running the node module:

```sh
git clone https://github.com/inovex/azure-iot-edge-demo
cd azure-iot-edge-demo/device
npm install
# Run the module using the IoT device's connection string
node sensor.js $YOUR_CONNECTION_STRING
```
