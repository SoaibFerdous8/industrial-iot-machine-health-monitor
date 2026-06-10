from opcua import Server
import paho.mqtt.client as mqtt
import threading
import time

server = Server()
server.set_endpoint('opc.tcp://0.0.0.0:4840/factory')
server.set_server_name('TeamB6 Factory Server')

uri = 'http://teamb6.factory'
idx = server.register_namespace(uri)

objects = server.get_objects_node()
factory = objects.add_object(idx, 'Factory')

machine1 = factory.add_object(idx, 'Machine1')
temp_var    = machine1.add_variable(idx, 'Temperature', 0.0)
hum_var     = machine1.add_variable(idx, 'Humidity', 0.0)
gas_var     = machine1.add_variable(idx, 'Gas', 0.0)

machine2 = factory.add_object(idx, 'Machine2')
sound_var   = machine2.add_variable(idx, 'Sound', 0.0)
vibration_var = machine2.add_variable(idx, 'Vibration', 0.0)

temp_var.set_writable()
hum_var.set_writable()
gas_var.set_writable()
sound_var.set_writable()
vibration_var.set_writable()

def on_message(client, userdata, msg):
    value = float(msg.payload.decode())
    topic = msg.topic
    if topic == "factory/machine1/temperature":
        temp_var.set_value(value)
    elif topic == "factory/machine1/humidity":
        hum_var.set_value(value)
    elif topic == "factory/machine1/gas":
        gas_var.set_value(value)
    elif topic == "factory/machine2/sound":
        sound_var.set_value(value)
    elif topic == "factory/machine2/vibration":
        vibration_var.set_value(value)
    print(f"OPC UA updated: {topic} = {value}")

def on_connect(client, userdata, flags, rc):
    client.subscribe("factory/#")

mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect("localhost", 1883, 60)

mqtt_thread = threading.Thread(target=mqttc.loop_forever)
mqtt_thread.daemon = True
mqtt_thread.start()

server.start()
print("OPC UA Server started at opc.tcp://0.0.0.0:4840/factory")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    server.stop()
