# Intro

This is repository of a innovation project done for Nokia. The idea is to build a framework which allows rapid development of different kinds of sensor management systems. The sensor could ultimately be anything. 

The data aquisiton functionality is being abstracted so that the system doesn't need to know what kind of a sensor has been attached to it.

The system handles all communication via MQTT messages. 

# Installation

The system consists of three parts: 1) Device and Sensor part 2) ManagementAttestor part 3) Management UI part. Each part can be run on separete devices. In fact, it is NOT recommended to run sensors and ManagementAttestor on the same device. The only requirement is that each part is using the same MQTT broker, so that they can communicate with each other.

## 1. Installing and running the Device and Sensor part

1.  Installing the necessary files

	a) Go to the folder /opt/ on the terminal

    b) Clone the repository using git: `sudo git clone https://github.com/teemvil/iot.git`. This downloads all the necessary library files.
    
    c) Navigate your way to the install folder at `iot/secure_sensor_management_system/install` and run the installation script: 
    ```
    sudo python3 install.py
    ```

    The install script creates iot.devices.service and iot.sensors.service files to etc/systemd/system. 
	
	The install script also creates two config files, `client_config.json` and `device_config.json`, to the folder `/etc/iotDevice/`. These config files are used as MQTT client configuration and as a specific device configuration. The device configuration file should contain the itemid of the pi on which the scripts are running on. MAKE SURE TO CHECK THAT THE MQTT CLIENT INFO AND THE ITEMID OF THE PI ARE CORRECT IN THESE FILES ONCE THEY ARE CREATED!!
    
    d) Enable the services using systemd:

    ```
    sudo systemctl enable iot.devices.service
    sudo systemctl start iot.devices.service
    ```

    ```
    sudo systemctl enable iot.sensors.service
    sudo systemctl start iot.sensors.service
    ```

2. Create sensor/implementations 

    a) To install IoTLibrary as a package, go to the folder `/opt/iot/secure_sensor_management_system/` and run the command `pip3 install .` 

    b) Create a new folder for the sensor under `/opt/iot/secure_sensor_management_system/`

    c) Create new sensor script. Most important thing is to inherit the BasicSensor from SensorManagementLibrary.
    
    ```python
    from SensorManagementLibrary.BasicSensor import BasicSensor
    ```

    d) Create configuration file for the sensor and name it as `sensor_config.json`. This file should be stored in the same folder as your sensor script. The file should include three fields like this:
    ```json
    {
        "name": "EXAMPLE RNGsensor",
        "frequency": 1,
        "prefix": "EXAMPLE"
    } 
    ```
	The fields denote:
	```
	name: The name of the sensor 
	frequency: The interval time between sending data values, in seconds
	prefix: The sensor's indentifying code for the MQTT data channel 
	```
    
    Fill the values in according to your sensor's needs.


3. Run the newly created script:

	You can run the sensor straight from the terminal thusly:
	```bash
	python3 YourNewSensor.py
	```
    
	To make the sensor start at device startup, add the sensor to the file `IotSensorStartup.py` in the folder `/opt/iot/secure_sensor_management_system/startup_scripts/`.	
	Like thus:
    ```python
        from YourNewSensor import YourNewSensor
        x = YourNewSensor()
        x.run()
    ```

## 2. Installing and running the ManagementAttestor part

1.  a) Go to the folder /opt/ on the terminal

    b) Clone the repository using git: `sudo git clone https://github.com/teemvil/iot.git`. This downloads all the necessary library files.
	
	c) Navigate your way to the install folder at `iot/secure_sensor_management_system/install` and run the installation script: 
    ```
    sudo python3 install.py
    ```

    The script creates two config files, `client_config.json` and `device_config.json` to the folder `/etc/iotDevice/`.These are used as MQTT client configuration and as a specific device configuration. MAKE SURE TO CHECK THAT THE MQTT CLIENT INFO IS CORRECT IN THE client_config.json FILE ONCE IT IS CREATED!!
	
	d) To install IoTLibrary as a package, go to the folder `/opt/iot/secure_sensor_management_system/` and run the command `pip3 install .`
	
	e) Navigate your way to the ManagementAttestor folder at `/opt/iot/secure_sensor_management_system/ManagementAttestor/` and add the correct ip and port addresses the file `manager_config.json`. The ip and port that you want to put there are the ones used by the attestation engine, which you should already have running somewhere.
	
	f) You can now run the Manager with the command `sudo python3 Manager.py`
	

## 3. Installing and running the Management UI part

1.  a) Go to the folder /opt/ on the terminal

    b) Clone the repository using git: `sudo git clone https://github.com/teemvil/iot.git`. This downloads all the necessary library files.
	
	c) Navigate your way to the website folder at `/opt/iot/secure_sensor_management_system/website/` and start the server using the command `npm start` 
	
	IF THIS DOES NOT WORK, MAKE SURE YOU HAVE NPM INSTALLED ON YOUR SYSTEM. You can install it with the command `sudo apt install npm nodejs` 
	
	d) You should now be able to access the management UI by going to the address `https://localhost:3000`




# Design

The system is build so that every class inherits a MQTT client from the IoTElement class. There is also a configuration file located in xxx which has all the necessary options to connect to the MQTT broker and send correct types of messages.

![device class diagram](documentation/pics/insidedevice.JPG)

# Data flow

When the system starts up it sends various MQTT messages to notify the broker about the state of the various subsystems. Firstly the validity of the device running the sensor script is checked. The sensor startup doesn't depend on the validity check. We can just see if the device is valid or not. 

![sequence diagram](documentation/pics/devicesequence.JPG)

## MQTT topic naming conventions

Sensors are named as `sensor/webcam`, `sensor/ir`, `sensor/lux`, `sensor/tof`.

### Management channel
```
management/
```

### Alert channel
```
alert/
```

### Data channels
```
prefix/<measurementtype>
```
Measurementtype here means the type of measured data. This could be array of pixels, temperature, distance etc


Most important payload fields:
itemid and event

How to name different events:

device startup

device validation start

device validation ok

device validation fail

sensor startup

manager startup
