from paho.mqtt import client as paho_mqtt_client
from datetime import datetime
from config import config


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)


class MqttClient:
    def __init__(self, config: config):
        """

        :type port: object
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
        def on_message(client, userdata, message):
            message = "Received message: " + str(message.payload.decode('UTF-8')) + " on topic: " + message.topic + " QoS: " + str(message.qos)
            print(message)
            with open('subscriber_log.txt', 'a') as out_file:
                out_file.write(f'{datetime.now()} {message}\n')

        result_list = []
        if not self.connected:
            self.connected()
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

# def simple_callback(client, userdata, msg):
#     print(f"simple_callback {client}; {userdata} Received `{msg.payload.decode()}` from `{msg.topic}` topic")

if __name__ == '__main__':
    print(config)
    # mqtt_client = MqttClient(config.broker, config.port, config.client_id)
    mqtt_client = MqttClient(config)
    mqtt_client.run_loop()
    # mqtt_client.connect()
    # mqtt_client.subscribe(config.topics)
    # mqtt_client.client.message_callback_add('test/#', simple_callback)
    # mqtt_client.loop()
    print(mqtt_client)

