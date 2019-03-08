# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import random
import time
import sys
import json
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
            protocol=IoTHubTransportProvider.MQTT,
            connection_string=None):
        self.client_protocol = protocol
        self.client= IoTHubModuleClient(connection_string, protocol)
        self.device_id= connection_string.split(";")[1].split("=")[1]
        # set the time until a message times out
        self.client.set_option("messageTimeout", MESSAGE_TIMEOUT)
        # input for sensor messages
        self.client.set_message_callback("sensor", self.receive_measurement_callback, self)

    # Forwards the message received onto the next stage in the process.
    def forward_event_to_output(self, outputQueueName, event, send_context):
        self.client.send_event_async(
            outputQueueName, event, send_confirmation_callback, send_context)

    def receive_measurement_callback(self, message):
        message_buffer = message.get_bytearray()
        size = len(message_buffer)
        content = message_buffer[:size].decode()
        # should contain json with keys "uuid", "device", "timestamp", "value", "unit"
        measurement = json.decode(content)
        print("Received measurement " + str(measurement))
        value = measurement["temperature"]
        timestamp = measurement["timestamp"]
        message_uuid = measurement["message_uuid"]
        device_id = measurement["device_id"]
        # if value>20:
        map_properties = message.properties()
        key_value_pair = map_properties.get_internals()
        print ( "    Properties: %s" % key_value_pair )
        self.forward_event_to_output("sensor", message, message_uuid)
        return IoTHubMessageDispositionResult.ACCEPTED


def main(protocol, connection_string):
    try:
        print ( "\nPython %s\n" % sys.version )
        print(text2art("inovex"))
        hub_manager = HubManager(protocol, connection_string)
        print("Waiting for messages...")
        while True:
            time.sleep(1)

    except IoTHubError as iothub_error:
        print ("Unexpected error %s from IoTHub" % iothub_error)
        return
    except KeyboardInterrupt:
        print ("IoTHubModuleClient sample stopped")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        msg="Please provide connection string as first argument. Should be placed in single quotes"
        sys.exit(msg)
    connection_string=sys.argv[1]
    print("Provided connection string was '" + connection_string + "'")
    main(PROTOCOL, connection_string)