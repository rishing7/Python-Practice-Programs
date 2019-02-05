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
# broker = "broker.hivemq.com"
# broker = "iot.eclipse.org"
client = mqtt.Client("Python1")   #create new instance

client.on_connect = on_connect
client.on_log = on_log
client.on_message = on_message

print("connecting to a broker ", broker)
client.connect(broker)
client.loop_start()
client.subscribe("house/sensor1")
client.publish("house/sensor1", "my first message")

time.sleep(4)
client.loop_stop()
client.disconnect()

# disconnect