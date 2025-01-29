import ssl,os
from paho import mqtt
import paho.mqtt.client as paho
import time, random
from dotenv import load_dotenv

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code: %d", reason_code)  

def on_publish(client, userdata, mid, reason_code, properties):
    print("Message ID: "+str(mid), f"Published from {userdata['location']}")
    
# Simulate temperature sensor
def read_temperature():
    return round(random.uniform(20, 35), 1)


load_dotenv()

HOST_NAME = os.getenv("HOST_NAME")
PORT = os.getenv("PORT")
USER_NAME = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")


sensor_data = {"location": "room1"}

client = paho.Client(protocol=paho.MQTTv5,
                    callback_api_version=paho.CallbackAPIVersion.VERSION2,
                    client_id="",
                    userdata=sensor_data)

client.on_publish = on_publish
client.on_connect = on_connect

client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set(f"{USER_NAME}", f"{PASSWORD}")
client.connect(f"{HOST_NAME}", int(PORT))

# Start the loop to process callbacks
client.loop_start()

while True:
    temperature = read_temperature()
    (rc, mid) = client.publish('sensors/temp', str(temperature), qos=1, retain=True)
    print(f"Published: {temperature}°C")
    time.sleep(5)
