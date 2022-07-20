import machine
import time
import pycom
from network import WLAN
from machine import Pin
from dht import DHT
from machine import deepsleep
import urequests as requests

TOKEN = "" # Ubidots token
DEVICE_LABEL = "heltec" # Device to send to
VARIABLE_LABEL_TEMPERATURE = "temperature"  # Variable for temperature
VARIABLE_LABEL_HUMIDITY = "humidity"  # Variable for humidity

WIFI_SSID = "" # WIFI SSID, has to be a 2.4 GHz network
WIFI_PASS = "" # WIFI Password
DELAY = 60  # Delay to use between sending data, in seconds

# DHT11 sensor
th = DHT(Pin('P23', mode=Pin.OPEN_DRAIN), 0)

# WiFi connection
wlan = WLAN(mode=WLAN.STA)
wlan.antenna(WLAN.INT_ANT)
wlan.connect(WIFI_SSID, auth=(WLAN.WPA2, WIFI_PASS), timeout=5000)
while not wlan.isconnected ():
    pass
print("Connected to Wifi\n")

# Builds the json to send the request
def build_json(variable, value):
    try:
        data = {variable: {"value": value}}
        return data
    except Exception as e:
        print(e)
        return None

# Sending data to Ubidots Restful Webserice
def sendData(device, variable, value):
    try:
        url = "http://industrial.api.ubidots.com/"
        url = url + "api/v1.6/devices/" + device
        headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
        data = build_json(variable, value)

        if data is not None:
            print(data)
            req = requests.request("POST", url, data=None, json=data, headers=headers)
            return req.json()
        else:
            pass
        print(req)
    except Exception as e:
        print(e)
        pass

while True:

    th = DHT(Pin('P23', mode=Pin.OPEN_DRAIN), 0)
    result = th.read()
    while not result.is_valid():
        time.sleep(.5)
        result = th.read()
    returnValue = sendData(DEVICE_LABEL, VARIABLE_LABEL_TEMPERATURE, result.temperature)
    time.sleep(DELAY)
    returnValue = sendData(DEVICE_LABEL, VARIABLE_LABEL_HUMIDITY, result.humidity)
    time.sleep(DELAY)
