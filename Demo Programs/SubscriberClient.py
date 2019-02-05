#!/usr/bin/env python3
import paho.mqtt.client as mqtt
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("/IN/JIO/CC/ REG_deviceID/Config")


def on_message(client, userdata, msg):
    v = msg.payload.decode()
    print(type(v))
    if msg.payload.decode() == "Hello world!":
        print("Yes!")
        client.disconnect()

client = mqtt.Client()
client.connect("52.66.238.191", 1883, 60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()