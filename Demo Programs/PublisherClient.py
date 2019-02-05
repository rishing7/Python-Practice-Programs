#!/usr/bin/env python3

import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("52.66.238.191",1883,60)
client.publish("/IN/JIO/CC/ REG_deviceID/Registe",'')
client.disconnect()