import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with code :", str(rc))
    #subscribe topic
    client.subscribe("Text/#")

def on_message(client, userdate, msg):
    print(str(msg.payload))

client = mqtt.Client()
# print(type(client))

client.on_connect = on_connect
client.onmessage = on_message

client.connect("m14.cloudmqtt.com", 18410, 60)
client.username_pw_set("")