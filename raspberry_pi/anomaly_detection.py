import paho.mqtt.client as mqtt
import numpy as np
from sklearn.ensemble import IsolationForest
from collections import deque

BROKER = "localhost"
PORT = 1883
WINDOW_SIZE = 50

TOPICS = [
    "factory/machine1/temperature",
    "factory/machine1/humidity",
    "factory/machine1/gas",
    "factory/machine2/sound",
    "factory/machine2/vibration"
]

buffers = {t: deque(maxlen=WINDOW_SIZE) for t in TOPICS}
models  = {t: None for t in TOPICS}

def train_model(topic):
    data = np.array(buffers[topic]).reshape(-1, 1)
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(data)
    models[topic] = model
    print(f"[MODEL] Trained on {topic}")

def on_message(client, userdata, msg):
    topic = msg.topic
    try:
        value = float(msg.payload.decode())
        if np.isnan(value):
            return
    except ValueError:
        return

    buffers[topic].append(value)

    if len(buffers[topic]) == WINDOW_SIZE and models[topic] is None:
        train_model(topic)

    if models[topic] is not None:
        prediction = models[topic].predict([[value]])
        status = "ANOMALY" if prediction[0] == -1 else "normal"
        if status == "ANOMALY":
            print(f"[ALERT] {topic} = {value} --> *** ANOMALY DETECTED ***")
        else:
            print(f"[OK]    {topic} = {value}")

        if len(buffers[topic]) == WINDOW_SIZE:
            train_model(topic)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message
client.connect(BROKER, PORT, 60)

for topic in TOPICS:
    client.subscribe(topic)
    print(f"Subscribed to {topic}")

print("\n[INFO] Waiting for data... (model trains after 50 readings per topic)\n")
client.loop_forever()
