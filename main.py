import logging
import os
from pydoc_data.topics import functions

import paho.mqtt.client as mqtt

import speaker_comm

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="speaker", protocol=mqtt.MQTTv5)

log = logging.getLogger()

mqtt_url = os.environ['MQTT_URL']
mqtt_port = int(os.environ['MQTT_PORT'])


functions = {
    "/state": speaker_comm.change_state,
    "/volume": speaker_comm.set_volume,
    "/sw": speaker_comm.set_sw,
    "/input": speaker_comm.set_input
}


def on_subscribe(client, userdata, mid, reason_code_list, properties):
    if reason_code_list[0].is_failure:
        log.error(f"Broker rejected you subscription: {reason_code_list[0]}")
    else:
        log.info(f"Broker granted the following QoS: {reason_code_list[0].value}")


def on_unsubscribe(client, userdata, mid, reason_code_list, properties):
    if len(reason_code_list) == 0 or not reason_code_list[0].is_failure:
        log.info("unsubscribe succeeded (if SUBACK is received in MQTTv3 it success)")
    else:
        log.error(f"Broker replied with failure: {reason_code_list[0]}")
    client.disconnect()


def on_message(client, userdata, message):
    log.debug(f"Inconming value {message.payload.decode()} for setting {functions[message.topic]}")
    try:
        log.debug(f"message: {message.topic}")
        functions[message.topic](int(message.payload.decode()))
        mqttc.publish("/settings", payload=speaker_comm.get_settings().to_json(), qos=2)
    except IOError:
        mqttc.publish("/error", payload="Request failed")
        log.exception(f"Request failed")


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        log.error(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
    else:
        for topic in functions:
            client.subscribe(topic)
            log.info(f"Subscribed to topic: {topic}")
        mqttc.publish("/settings", payload=speaker_comm.get_settings().to_json())


def on_publish(client, userdata, mid, reason_code, properties):
    log.debug(f"message published {mid}")


def get_client():
    return mqttc


def main():
    logging.basicConfig(
        level=logging.DEBUG,  # Set the log level
        format='%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s',  # Define the format
        datefmt='%Y-%m-%d %H:%M:%S'  # Define the date format with microseconds
    )
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.on_subscribe = on_subscribe
    mqttc.on_unsubscribe = on_unsubscribe
    mqttc.on_publish = on_publish

    mqttc.user_data_set([])
    log.info("mqtt server started")
    mqttc.connect(mqtt_url, mqtt_port)
    mqttc.loop_forever()


if __name__ == '__main__':
    main()
