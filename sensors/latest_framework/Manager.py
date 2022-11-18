from IoTElement import IoTElement
from datetime import datetime
import json



class Manager(IoTElement):
    def __init__(self):
        super().__init__()
        self.client.subscribe('management')
        self.client.on_connect = self.__on_connect
        self.client.on_message = self.__on_message
        self.client.loop_forever()
        self.__start_manager(self.config)

    def __attest_validate(self, json_update):
        json_object = json_update
        json_object["event"] = "validating device"
        json_object["message"] = "Device validation in process"
        self.client.publish(f"management/verify", json.dumps(json_object))

    def __on_connect(self, client, userdata, flags, rc):
        print("devmanager connected with result code " + str(rc))
        json_object = self.config
        json_object["message"] = "Sensor manager running"
        json_object["event"] = "starting sensor manager"
        json_object["timestamp"] = self.__get_time_stamp()
        self.client.publish("management", json.dumps(json_object))
        #print(json_object)

    def __on_message(self, client, userdata, msg):
        decoded_message = str(msg.payload.decode("utf-8"))
        json_object = json.loads(decoded_message)
        #print(json_object)

        if msg.topic == "management" and json_object["hostname"] == "iotpi012":
            print("iotpi12 functionality")

        if msg.topic == "management" and json_object["hostname"] == "iotpi014":
            print("iotpi14 functionality")

        if msg.topic == "management" and json_object["hostname"] == "iotpi015":
            print("iotpi15 functionality")

        if msg.topic == "management" and json_object["hostname"] == "iotpi016":
            print("iotpi16 functionality")

    def __get_time_stamp(self):
        now = datetime.now()
        date_time = now.strftime("%d.%m.%Y, %H:%M:%S")
        return date_time

    def run(self):
        print("manager run")

    def publish_datat(self, json_update):
        self.client.publish("management", "astddfsa")
