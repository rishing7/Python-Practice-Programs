import time
import sys
import os
import paho.mqtt.client as paho
sys.path.append("/home/pi/Adafruit_Python_CharLCD")
import Adafruit_CharLCD as LCD
import Adafruit_GPIO.MCP230xx as MCP

### Define MCP pins connected to LCD
lcd_rs = 6
lcd_en = 4
lcd_d4 = 3
lcd_d5 = 2
lcd_d6 = 1
lcd_d7 = 0
lcd_backlight = None

### Define LCD type
lcd_columns = 20
lcd_rows = 4

### Initialize MCP23017 for LCD
gpiomcp = MCP.MCP23017(0x20, busnum=1)

### Initialize LCD panel parameters
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight, gpio=gpiomcp)
lcd.show_cursor(False)
lcd.blink(False)
lcd.clear()

### DATE
def on_message_date(mosq, obj, msg):
    lcd.set_cursor(0,0)
    lcd.message(str(msg.payload))

### TIME
def on_message_time(mosq, obj, msg):
    lcd.set_cursor(0,2)
    lcd.message(str(msg.payload))

### RELAY
def on_message_relay(mosq, obj, msg):
    if (str(msg.payload)[3]) == '0':
        lcd.set_cursor(7,2)
        lcd.message("RL1= 0 RL2= 0")
    elif (str(msg.payload)[3]) == '1':
        lcd.set_cursor(7,2)
        lcd.message("RL1= 1 RL2= 0")
    elif (str(msg.payload)[3]) == '2':
        lcd.set_cursor(7,2)
        lcd.message("RL1= 0 RL2= 1")
    elif (str(msg.payload)[3]) == '3':
        lcd.set_cursor(7,2)
        lcd.message("RL1= 1 RL2= 1")
    else:
        lcd.set_cursor(7,2)
        lcd.message("RELAYs ERROR!")

### PUBLIC IP
def on_message_pubip(mosq, obj, msg):
    lcd.set_cursor(0,1)
    lcd.message("                    ")
    lcd.set_cursor(0,1)
    lcd.message("IP = "+str(msg.payload)[0:14])

### TEMPERATURE
def on_message_temp(mosq, obj, msg):
    lcd.set_cursor(0,3)
    lcd.message(str(msg.payload)[0:4]+chr(223)+"C")

### HUMIDITY
def on_message_humi(mosq, obj, msg):
    lcd.set_cursor(7,3)
    lcd.message(str(msg.payload)[0:4]+chr(37))

### PRESSURE
def on_message_pres(mosq, obj, msg):
    lcd.set_cursor(13,3)
    lcd.message(str(msg.payload)+"hPa")

### topic message
def on_message(mosq, obj, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

mqttc = paho.Client()

#Add message callbacks that will only trigger on a specific   subscription    match
mqttc.message_callback_add('iDomus/Time', on_message_time)
mqttc.message_callback_add('iDomus/Date', on_message_date)
mqttc.message_callback_add('iDomus/PubIPRead', on_message_pubip)
mqttc.message_callback_add('iDomus/RPiS/Sens1/Temp', on_message_temp)
mqttc.message_callback_add('iDomus/RPiS/Sens1/Humi', on_message_humi)
mqttc.message_callback_add('iDomus/RPiN/Sens2/Pres', on_message_pres)
mqttc.message_callback_add('iDomus/RPiS/Rel1/Read', on_message_relay)
mqttc.on_message = on_message
mqttc.connect("10.0.2.10", 1883, 30)
mqttc.subscribe("iDomus/#")

mqttc.loop_forever()