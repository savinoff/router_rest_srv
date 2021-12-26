from paho.mqtt import client as paho_mqtt_client
from datetime import datetime
from config import config
from Classes.db import db


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)


def on_message(client, userdata, message):
    message_res = "Received message: " + str(message.payload.decode('UTF-8')) + " on topic: " + message.topic + " QoS: " + str(message.qos)
    # print(message_res)
    with open('subscriber_log.txt', 'a') as out_file:
        out_file.write(f'{datetime.now()} {message_res}\n')
    topic_l = str(message.topic).split('/')
    device, sensor = None, None
    if len(topic_l) > 3 and topic_l[0] == 'devices' and topic_l[2] == 'sensors':
        device = topic_l[1]
        sensor = topic_l[3]
        value = float(message.payload.decode('UTF-8'))
        db.add_sensor_value(device_key=device, sensor_key=sensor, value=value)
    else:
        print(f'{datetime.now()} {message_res}')


class MqttClient:
    def __init__(self, config: config):
        """
        """
        self.config = config
        self.client: paho_mqtt_client = None
        self.broker = config.broker
        self.port = config.port
        self.client_id = config.client_id
        self.connected = str(None)

    def connect(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
                self.connected = True
            else:
                print("Failed to connect, return code %d\n", rc)
        # Set Connecting Client ID
        self.client = paho_mqtt_client.Client(self.client_id)
        # client.username_pw_set(username, password)
        self.client.on_connect = on_connect
        self.client.connect(self.broker, self.port)
        
    def subscribe(self, topics: list) -> list:
        result_list = []
        if not self.connected:
            self.connect()
        for topic in topics:
            print(f'Subscribing to {topic}')
            subscribe_result = self.client.subscribe(topic)
            callback_result = self.client.message_callback_add(topic, on_message)
            print(f'Subscribe result: {subscribe_result}, callback_result = {callback_result}')
            result_list.append((topic, subscribe_result))
        self.client.on_message = on_message
        return result_list

    def run_loop(self):
        """
        connect, subscribe and loop mqtt client with config
        """
        self.connect()
        self.subscribe(self.config.topics)
        self.loop()

    def loop(self):
        self.client.loop_forever(timeout=5.0)


if __name__ == '__main__':
    print(config)
    mqtt_client = MqttClient(config)
    mqtt_client.run_loop()
    print(mqtt_client)

