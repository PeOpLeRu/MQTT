import paho.mqtt.client as mqtt_client
import random
import time
import serial

UNIQUE_ID = 998
port = "COM7"
ser = serial.Serial(port, 9600)

min_ =0
min_illum = 0
max_illum = 0
def illum(data):
    global max_illum
    global min_illum
    if(data>=max_illum):
        max_illum = data
    else:
        min_illum = data
    mean = (max_illum+min_illum)/2
    if (mean>=50):
        ser.write("1".encode())
        time.sleep(5)
    else:
        ser.write("0".encode())
        time.sleep(5)
    print(min_illum, " ", max_illum, "mean = ", mean)



def dec_inc(data):
    print(f"recieved sensor level{ data}")
    
    # print(type(data))
    global min_
    if(data <=10 and min_<=data):
        min_ = data
        ser.write("1".encode())
    else:
        ser.write("0".encode())
        # time.sleep(2)
    min_ = data 



def write(data):       
    print(f"recieved command {data}")
    if (data == "1"):
        ser.write("1".encode())
        time.sleep(2)
    if (data =="0"):
        ser.write("0".encode())
        time.sleep(2)

def on_message(client, data, message):
    data = float(message.payload.decode("utf-8"))
    
    # topic = str(message.topic.decode("utf-8"))
    # print(f"Received message on topic {data}")
    # write(data)
    dec_inc(data)
    illum(data)
    return data
    


broker = "broker.emqx.io" 

client = mqtt_client.Client(f"lab_{random.randint(10000, 99999)}")
client.on_message = on_message


try:
    client.connect(broker)
except Exception:
    print("Failed to connect. Check network")
    exit()    

client.loop_start()

# while not client.is_connected():

print("Subscribing")    

client.subscribe(f'lab/{UNIQUE_ID}/photo/instant')
client.subscribe(f'lab/{UNIQUE_ID}/photo/average')
    
client.subscribe(f'lab/{UNIQUE_ID}/photo/min')
client.subscribe(f'lab/{UNIQUE_ID}/photo/max')
time.sleep(600)
client.disconnect()
client.loop_stop()
print("Stop communication")