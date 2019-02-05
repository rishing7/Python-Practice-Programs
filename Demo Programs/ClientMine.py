import paho.mqtt.client as mqtt   #import the client
import time
def on_log(client, userdata, level, buf):
    print("logs: ", buf)
def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("Connection OK!!!")
    else:
        print("Bad Connection")
def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnected result code", str(rc))
broker = "test.mosquitto.org"
broker = "192.168.2.11"
client = mqtt.Client("Python1")    #create new instance

client.on_connect = on_connect
client.on_disconnect = on_disconnect  #bind call back function
client.on_log = on_log

print("Connecting to broker", broker)
# imei = 1234567
# uname = 'rishi'
# psw = '123'
client.loop_start()                 #start loop
client.connect(broker)
client.publish("IN/JIO/CC/ REG_deviceID/")
client.subscribe(" /IN/JIO/CC/ REG_deviceID/Config")
time.sleep(1)
client.loop_stop()
client.disconnect()