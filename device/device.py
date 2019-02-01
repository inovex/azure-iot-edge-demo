# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import random
import time
import sys
import os
import uuid
import json
import iothub_client
# pylint: disable=E0611
from iothub_client import IoTHubModuleClient, IoTHubClientError, IoTHubTransportProvider
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError
from ds18b20 import DS18B20
from art import text2art
from datetime import datetime

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
        return self.ds.temperature()


class HubManager(object):

    def __init__(
            self,
            protocol=IoTHubTransportProvider.MQTT,
            connection_string=None):
        self.client_protocol = protocol
        self.client= IoTHubModuleClient(connection_string, protocol)
        self.device_id= connection_string.split(";")[1].split("=")[1]
        # set the time until a message times out
        self.client.set_option("messageTimeout", MESSAGE_TIMEOUT)

    def send_confirmation_callback(self, message, result, user_context):
        print("IoT Hub responded to message " + str(user_context) 
              + " with status " + str(result))

    
    def send_measurement(self, value, timestamp):
        message_uuid=uuid.uuid1()
        contents={
            "uuid": str(message_uuid),
            "device": self.device_id,
            "timestamp": str(timestamp),
            "value": value,
            "unit": "°C"
            }
        message=IoTHubMessage(json.dumps(contents))
        print("Sending message " + str(message_uuid) + " with contents " + str(contents))
        self.client.send_event_async(message, self.send_confirmation_callback, message_uuid)


def main(protocol, sensor=None, connection_string=None):
    try:
        print("\nPython %s\n" % sys.version)
        print(text2art("inovex"))
        hub_manager = HubManager(protocol, connection_string)
        while True:
            measurement = sensor.measure()
            hub_manager.send_measurement(measurement, datetime.utcnow())
            time.sleep(1)


    except IoTHubError as iothub_error:
        print("Unexpected error %s from IoTHub" % iothub_error)
        return
    except KeyboardInterrupt:
        print("IoTHubModuleClient sample stopped")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        msg= "Please provide run mode as first argument. Can be one of 'sensor' or 'simulate'"
        sys.exit(msg)
    elif len(sys.argv) < 3:
        msg="Please provide connection string as second argument. Should be placed in single quotes"
        sys.exit(msg)
    connection_string=sys.argv[2]
    print("Provided connection string was '" + connection_string + "'")
    if sys.argv[1] == "sensor":
        main(PROTOCOL, RealSensor(), connection_string)
    elif sys.argv[1] == "simulate":
        main(PROTOCOL, SimulatedSensor(), connection_string)
    else:
        sys.exit("Unknown run mode '" + sys.argv[1] + "'.")
