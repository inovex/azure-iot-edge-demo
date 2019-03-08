http://www.circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial/


## setup

* Install dependencies: `curl -sL http://deb.nodesource.com/setup_8.x | sudo -E bash && sudo apt-get install -y nodejs`
* `sudo $(echo "dtoverlay=w1–gpio" >> /boot/config.txt)`
* `sudo reboot`
* Check out this repo: `git clone https://github.com/inovex/azure-iot-edge-demo`
* `cd azure-iot-edge-demo/device-nodejs`
* `node sensor.js $(cat /etc/edge/connection_string)`
* Create your device