import device
import paho.mqtt.client as mqtt
import json

client = mqtt.Client()
client.connect('127.0.0.1')
sensor = device


def on_message(_client, userdata, msg):
    # Listen to management topic.
    x = json.loads(msg.payload)

    # This is just horrible xD
    if x['operation'] == 'verify' and x['type'] != 'sensor-startup':
        sensor.validate()
    elif x['operation'] == 'verify' and x['type'] == 'sensor-startup' and x['result'] == 'success':
        sensor.measure_stuff()


def send_alert():
    client.publish('alert', json.dumps({'message': 'verify not successful'}))


def stop_sensor():
    pass


def reboot():
    pass


def run():
    client.subscribe('management')
    client.on_message = on_message

    client.loop_forever()
