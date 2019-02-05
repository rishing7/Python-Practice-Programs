import paho.mqtt.client as mqtt
import time

def on_log(client, userdata, level, buf):
    print("logs:", buf)

def on_connect(client, userdata, flags, rc):
    if(rc==0):
        print("Connection is OK!!")
    else:
        print("Bad Connectio, Try Again!!")

def on_message(client, userdata, msg):
    if __name__ == '__main__':
        topic = msg.topic
        m_decode = str(msg.payload.decode("utf-8"))
        print("message received", m_decode)
        print("message topic", topic)

broker = "test.mosquitto.org"
mqttc1 = mqtt.Client("Client1")
# mqttc2 = mqtt.Client("Client2")
mqttc3 = mqtt.Client("Client3")
mqttc3.on_connect = on_connect
mqttc3.on_message = on_message
mqttc3.on_log = on_log

mqttc1.connect(broker, 1883)
# mqttc2.connect(broker, 1883, 60)
mqttc3.connect(broker, 1883)
mqttc3.loop_start()

mqttc3.subscribe("hello/world1")
mqttc1.publish("hello/world1", "Hello World")
# mqttc2.publish("hello/world2", "Hello World")
time.sleep(4)
mqttc3.loop_stop()