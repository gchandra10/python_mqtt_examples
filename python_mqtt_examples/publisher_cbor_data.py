import ssl, os, cbor2
from paho import mqtt
import paho.mqtt.client as paho
import time, random
from dotenv import load_dotenv

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(f"Connected to MQTT Broker at {HOST_NAME}!")
        # Add connection status to userdata
        userdata['connected'] = True
    else:
        print(f"Failed to connect, reason code: {reason_code}")
        userdata['connected'] = False

def on_publish(client, userdata, mid, reason_code, properties):
    print(f"Message ID: {mid}, Published from {userdata['location']}, Status: {reason_code}")
    
def on_disconnect(client, userdata, reason_code, properties, packet):
    print(f"Disconnected with reason code: {reason_code}")
    userdata['connected'] = False

# Simulate temperature sensor with more realistic values
def read_temperature():
    base_temp = 24.0  # Room temperature baseline
    variation = random.uniform(-2.0, 2.0)
    return round(base_temp + variation, 1)

def create_sensor_payload():
    return {
        "temperature": read_temperature(),
        "humidity": random.randint(45, 75),
        "device_id": "sensor_123",
        "timestamp": int(time.time())
    }

# Load environment variables
load_dotenv()

HOST_NAME = os.getenv("HOST_NAME")
PORT = int(os.getenv("PORT", 8883))  # Default to 8883 for TLS
USER_NAME = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")

# Initialize userdata with more information
sensor_data = {
    "location": "room1",
    "connected": False
}

# Client setup with clean session
client = paho.Client(
    protocol=paho.MQTTv5,
    callback_api_version=paho.CallbackAPIVersion.VERSION2,
    client_id=f"sensor_{random.randint(0, 1000)}",  # Random client ID
    userdata=sensor_data
)

# Set callbacks
client.on_publish = on_publish
client.on_connect = on_connect
client.on_disconnect = on_disconnect

# Set up TLS
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set(USER_NAME, PASSWORD)

try:
    client.connect(HOST_NAME, PORT)
    
    # loop_start triggers the on_message, on_publish and on_connect callbacks
    client.loop_start()

    # Wait for connection
    time.sleep(1)

    if sensor_data['connected']:
        # Create and publish payload
        payload = create_sensor_payload()
        cbor_data = cbor2.dumps(payload)
        
        result = client.publish(
            'measure/all', 
            cbor_data, 
            qos=1, 
            retain=True
        )
        print(f"Published: {payload}, Result: {result}")
    else:
        print("Not connected to broker, cannot publish")

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    # Clean disconnect
    client.loop_stop()
    client.disconnect()