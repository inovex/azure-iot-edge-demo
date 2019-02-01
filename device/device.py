# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import random
import time
import sys
import os
import iothub_client
# pylint: disable=E0611
from iothub_client import IoTHubModuleClient, IoTHubClientError, IoTHubTransportProvider
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError
from sensor.DS18B20 import DS18B20

# messageTimeout - the maximum time in milliseconds until a message times out.
# The timeout period starts at IoTHubModuleClient.send_event_async.
# By default, messages do not expire.
MESSAGE_TIMEOUT = 10000

# global counters
RECEIVE_CALLBACKS = 0
SEND_CALLBACKS = 0

# Choose HTTP, AMQP or MQTT as transport protocol.  Currently only MQTT is supported.
PROTOCOL = IoTHubTransportProvider.MQTT


class SimulatedSensor:
    def measure(self):
        return random.randint(-5, 35)


class RealSensor:

    def __init__(self):
        sensor_address = os.environ.get("SENSOR_ADDRESS")
        if sensor_address is None:
            raise EnvironmentError("Variable SENSOR_ADDRESS must be set")
        self.ds = DS18B20(sensor_address)

    def measure(self):
        return self.ds.temperature().C


class HubManager(object):

    def __init__(
            self,
            protocol=IoTHubTransportProvider.MQTT):
        self.client_protocol = protocol
        self.client = IoTHubModuleClient()
        self.client.create_from_environment(protocol)

        # set the time until a message times out
        self.client.set_option("messageTimeout", MESSAGE_TIMEOUT)


def main(protocol):
    try:
        print("\nPython %s\n" % sys.version)
        print("IoT Hub Client for Python")

        hub_manager = HubManager(protocol)

        print("Starting the IoT Hub Python sample using protocol %s..." %
              hub_manager.client_protocol)
  
        while True:
            time.sleep(1)


    except IoTHubError as iothub_error:
        print("Unexpected error %s from IoTHub" % iothub_error)
        return
    except KeyboardInterrupt:
        print("IoTHubModuleClient sample stopped")


if __name__ == '__main__':
    main(PROTOCOL)
