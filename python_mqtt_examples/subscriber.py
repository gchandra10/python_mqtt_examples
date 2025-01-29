import ssl,os
from paho import mqtt
import paho.mqtt.client as paho
from dotenv import load_dotenv

def on_subscribe(client, userdata, mid, granted_qos, properties):  # Updated for MQTTv5
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_message(client, userdata, msg):
    # Decode the payload from bytes to string
    payload = msg.payload.decode()
    print(f"Topic: {msg.topic}, QoS: {msg.qos}, Temperature: {payload}°C")    

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected to MQTT Broker!")
        # Subscribe after connection
        client.subscribe("sensors/#", qos=1)
    else:
        print(f"Failed to connect, return code: {reason_code}")  

client = paho.Client(
    protocol=paho.MQTTv5,
    callback_api_version=paho.CallbackAPIVersion.VERSION2,
    client_id="",
    userdata=None
)

load_dotenv()

HOST_NAME = os.getenv("HOST_NAME")
PORT = os.getenv("PORT")
USER_NAME = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")

# Set callbacks
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_message = on_message

# Set TLS and credentials before connecting
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set(f"{USER_NAME}", f"{PASSWORD}")
client.connect(f"{HOST_NAME}", int(PORT), clean_start=False)

client.loop_forever()