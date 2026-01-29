# Python MQTT Examples

Create free account [hivemq.com](https://console.hivemq.cloud/)


**Open VSCode IOT Workspace**

- Fork and Clone the project

```
git clone <your repo>
```

```
cd python_mqtt_examples 
```

**Rename the .env_template to .env**

```
Update the values
```

**Update Repo**

```
uv sync
```

**Run Publisher**

Goto Terminal

```
uv run python publisher.py
```

Open Second Terminal

**Run Subscriber**
```
uv run python subscriber.py
```

**Add missing libraries (example)**

```
uv add paho-mqtt
uv add python-dotenv
```