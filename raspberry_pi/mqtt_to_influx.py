import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

TOKEN  = "yfzAhmLTPzkT4hsaHe2Z17A1M12acTYqXzHwLu7R7aHqNElxje_yVv8tjvcoKjKzPkYFv0wxfhaASar3yR8nQQ=="
ORG    = "teamb6"
BUCKET = "factory_sensors"
URL    = "http://localhost:8086"

client = InfluxDBClient(url=URL, token=TOKEN, org=ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

TOPICS = [
    "factory/machine1/temperature",
    "factory/machine1/humidity",
    "factory/machine1/gas",
    "factory/machine2/sound",
    "factory/machine2/vibration"
]

def on_message(client, userdata, msg):
    value = float(msg.payload.decode())
    parts = msg.topic.split("/")
    machine = parts[1]
    measurement = parts[2]
    point = Point(measurement).tag("machine", machine).field("value", value)
    write_api.write(bucket=BUCKET, org=ORG, record=point)
    print(f"Written: {machine} {measurement} = {value}")

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    for topic in TOPICS:
        client.subscribe(topic)

mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect("localhost", 1883, 60)
mqttc.loop_forever()
