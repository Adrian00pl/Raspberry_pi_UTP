import time
import ds18x20
import esp
import machine
import micropython
import network
import onewire
import ubinascii
from machine import Pin
from umqttsimple import MQTTClient
import gc

esp.osdebug(None)
gc.collect()

state = machine.Pin(25, machine.Pin.IN)
windowState = "0"  # Z - zamknięte, O - Otwarte

ssid = ''
password = ''
mqtt_server = ''

client_id = ubinascii.hexlify(machine.unique_id())

topic_pub_temp = b'sensor/temp'

last_message = 0
message_interval = 5

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)
print('Connection successful')


def connect_mqtt():
    global client_id, mqtt_server
    client = MQTTClient(client_id, mqtt_server)
    client.connect()
    print('Connected to %s MQTT broker' % (mqtt_server))
    return client


def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()


try:
    client = connect_mqtt()
except OSError as e:
    restart_and_reconnect()

while True:
    try:
        if (time.time() - last_message) > message_interval:
            if state.value() == 0:
                windowState = "0"
            else:
                windowState = "1"
            client.publish(topic_pub_temp, windowState)
            last_message = time.time()
    except OSError as e:
        restart_and_reconnect()
