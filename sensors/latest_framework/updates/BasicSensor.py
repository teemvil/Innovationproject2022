from device.IoTElement import IoTElement
from datetime import datetime
import json
import pathlib

class BasicSensor(IoTElement):

    def __init__(self):
        super().__init__()
        path = pathlib.Path(__file__).resolve().parent
        self.sensor_config = self.read_config_file(
            f"{path}/sensor_config.json")
        self.sensor_name = self.sensor_config["name"]
        self.frequency = self.sensor_config["frequency"]

        self.message["sensor"]["name"] = self.sensor_name
        self.message["event"] = "sensor startup"
        self.message["message"] = "Sensor " + self.sensor_name + \
            " started on "+self.message["device"]["hostname"]
        self.message["sensor"]["starttimestamp"] = self.__get_time_stamp()
        self.message["messagetimestamp"] = self.__get_time_stamp()
        self.client.publish("management", json.dumps(self.message))

    def publish_data(self, data, data_type):
        topic = self.sensor_config["prefix"]+"/"+data_type
        self.client.publish(topic, payload=data)

    def __get_time_stamp(self):
        now = datetime.now()
        date_time = now.strftime("%d.%m.%Y, %H:%M:%S")
        return date_time
