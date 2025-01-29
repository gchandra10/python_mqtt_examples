import ssl, os, cbor2
from paho import mqtt
import paho.mqtt.client as paho
from dotenv import load_dotenv
import time

def on_subscribe(client, userdata, mid, granted_qos, properties):
    print(f"Subscribed with Message ID: {mid}")
    for i, qos in enumerate(granted_qos):
        print(f"Granted QoS level {qos} for subscription {i+1}")

def on_message(client, userdata, msg):
    try:
        # Decode CBOR payload
        decoded_payload = cbor2.loads(msg.payload)
        
        # Extract and validate message components
        temperature = decoded_payload.get('temperature')
        humidity = decoded_payload.get('humidity')
        device_id = decoded_payload.get('device_id')
        timestamp = decoded_payload.get('timestamp')
        
        print(f"""
Received Message:
  Topic: {msg.topic}
  QoS: {msg.qos}
  Device ID: {device_id}
  Temperature: {temperature}°C
  Humidity: {humidity}%
  Timestamp: {timestamp}
        """)
        
        # Add your message processing logic here
        if temperature > 30:
            print("High temperature alert!")
            
    except cbor2.CBORDecodeError as e:
        print(f"CBOR decoding error: {e}")
    except Exception as e:
        print(f"Error processing message: {e}")

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(f"Connected successfully to {HOST_NAME}")
        # Subscribe to topics
        client.subscribe([
            ("measure/all", 1),  # QoS 1
            # Add more topic subscriptions as needed
        ])
    else:
        print(f"Connection failed with reason code: {reason_code}")

def on_disconnect(client, userdata, reason_code, properties):
    print(f"Disconnected with reason code: {reason_code}")
    if reason_code != 0:
        print("Unexpected disconnection. Attempting to reconnect...")

# Load environment variables
load_dotenv()

HOST_NAME = os.getenv("HOST_NAME")
PORT = int(os.getenv("PORT", 8883))  # Default to 8883 for TLS
USER_NAME = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")

# Initialize client with persistent session
client = paho.Client(
    protocol=paho.MQTTv5,
    callback_api_version=paho.CallbackAPIVersion.VERSION2,
    client_id="garage_subscriber",  # Fixed client ID for persistent session
    userdata={"location": "garage"}
)

# Set callbacks
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_disconnect = on_disconnect

# Set TLS configuration
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set(USER_NAME, PASSWORD)

try:
    client.connect(
        HOST_NAME, 
        PORT,
        keepalive=60,
        clean_start=False
    )
    
    # Start the loop
    client.loop_forever()  # Using loop_forever() for blocking operation

except KeyboardInterrupt:
    print("\nDisconnecting from broker")
    client.disconnect()
    client.loop_stop()
    
except Exception as e:
    print(f"Connection error: {e}")
    client.loop_stop()