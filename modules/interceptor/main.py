# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import os
import random
import time
import datetime
import sys
import json
import uuid
import iothub_client
# pylint: disable=E0611
from iothub_client import IoTHubModuleClient, IoTHubClientError, IoTHubTransportProvider
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError
from art import text2art

# messageTimeout - the maximum time in milliseconds until a message times out.
# The timeout period starts at IoTHubModuleClient.send_event_async.
# By default, messages do not expire.
MESSAGE_TIMEOUT = 10000

# Choose HTTP, AMQP or MQTT as transport protocol.  Currently only MQTT is supported.
PROTOCOL = IoTHubTransportProvider.MQTT

# Callback received when the message that we're forwarding is processed.
def send_confirmation_callback(message, result, user_context):
    print("IoT Hub responded to message " + str(user_context)
          + " with status " + str(result))

class HubManager(object):

    def __init__(
            self,
            protocol=IoTHubTransportProvider.MQTT):
        self.client_protocol = protocol
    
        self.client = IoTHubModuleClient()
        self.client.create_from_environment(protocol)
        self.device_id = os.getenv("IOTEDGE_DEVICEID", "err")
        # set the time until a message times out
        self.client.set_option("messageTimeout", MESSAGE_TIMEOUT)
        # input for sensor messages
        self.client.set_message_callback("sensor", receive_message_callback, self)
        self._received_measurements = {}
        self._last_sent_measurements = {}

    # Forwards the message received onto the next stage in the process.
    def forward_event_to_output(self, outputQueueName, event, send_context):
        self.client.send_event_async(
            outputQueueName, event, send_confirmation_callback, send_context)

    # This method is responsible for everything to do with message contents
    def handle_measurement(self, measurement):
        message_uuid = measurement["message_uuid"]
        device_id = measurement["device_id"]
        if device_id not in self._received_measurements:
            self._received_measurements[device_id] = []
        self._received_measurements[device_id] += [measurement["temperature"]]
        contents = {k:v for k, v in measurement.items()}
        contents["forward_device"] = self.device_id
        forward_message = IoTHubMessage(json.dumps(contents))
        self.forward_event_to_output("sensor", forward_message, message_uuid)

def receive_message_callback(message, hubManager):
    message_buffer = message.get_bytearray()
    size = len(message_buffer)
    content = message_buffer[:size].decode()
    measurement = json.loads(content)
    print("Received measurement " + str(measurement))
    hubManager.handle_measurement(measurement)
    return IoTHubMessageDispositionResult.ACCEPTED

def main(protocol):
    try:
        print("\nPython %s\n" % sys.version)
        print(text2art("inovex"))
        hub_manager = HubManager(protocol)
        print("Waiting for messages...")
        while True:
            time.sleep(1)

    except IoTHubError as iothub_error:
        print("Unexpected error %s from IoTHub" % iothub_error)
        return
    except KeyboardInterrupt:
        print("IoTHubModuleClient sample stopped")

if __name__ == '__main__':
    main(PROTOCOL)