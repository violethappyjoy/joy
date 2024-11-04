import os
import paho.mqtt.client as mqtt
from pymongo import MongoClient
import json

MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient("MONGO_URI")
db = client.stress_detection
collection = db.sensor_data


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    client.subscribe("sensors/#")


def on_message(client, userdata, msg):
    print(f"Received message on {msg.topic}: {msg.payload}")
    # Store data in MongoDB
    data = json.loads(msg.payload.decode())
    collection.insert_one(data)


mqtt_client = mqtt.Client(transport="websockets")
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_forever()
