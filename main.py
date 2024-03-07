# print("Hello")
import sys
from Adafruit_IO import MQTTClient
import time
import random
from simpleAI import *
from uart import *

AIO_FEED_IDs = ["button1", "button2"]
AIO_USERNAME = "NPAnh"
AIO_KEY = "aio_gWIA19BHnsanudG2d7M4oxVErObP"

def connected(client):
    print("Ket noi thanh cong ...")
    for topic in AIO_FEED_IDs:
        client.subscribe(topic)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Nhan du lieu: " + payload + " ,feed id:" + feed_id)

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()
counter = 10
sensor_type = 0
counter_ai = 5
ai_result = ""

while True:
    counter = counter -1
    if counter <= 0:
        counter = 10
        #TODO
        print("Random data is publishing...")
        if sensor_type == 0:
            print("Temperature...")
            temp = random.randint(10,20)
            client.publish("sensor1", temp)
            sensor_type = 1
        elif sensor_type == 1:
            print("Humidity...")
            humi = random.randint(50,70)
            client.publish("sensor2", humi)
            sensor_type = 2
        elif sensor_type == 2:
            print("Light...")
            light = random.randint(100, 500)
            client.publish("sensor3", light)
            sensor_type = 0
    counter_ai = counter_ai - 1
    if counter_ai <= 0:
        counter_ai = 5
        prev_ai = ai_result
        ai_result = image_detector()
        if prev_ai != ai_result:
            client.publish("AI", ai_result)    
        print("AI_Output: ", ai_result)
        
    readSerial(client)
    # data = ser.readline().decode('utf-8')
    # print(f'Received: {data}', end='')
    time.sleep(1)
    # pass
    # Listen to the keyboard for presses.
    # keyboard_input = cv2.waitKey(1)

    # # 27 is the ASCII for the esc key on your keyboard.
    # if keyboard_input == 27:
    #     break
