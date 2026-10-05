import network
import time
from machine import Pin
from umqtt.simple import MQTTClient

# הגדרות רשת
WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASS = "YOUR_WIFI_PASSWORD"

# הגדרות MQTT (כתובת ה-IP של ה-Home Assistant שלך)
MQTT_BROKER = "192.168.0.103"
MQTT_USER = "esp32"
MQTT_PASS = "YOUR_PASSWORD"
CLIENT_ID = "esp32_livingroom"

# נושאי MQTT (Topics)
TOPIC_STATE_LED = b"home/esp32/led/state"
TOPIC_SET_LED = b"home/esp32/led/set"
TOPIC_SENSOR = b"home/esp32/sensor/temp"

led = Pin(2, Pin.OUT)  # ברוב כרטיסי ESP32 ה-LED המובנה ב-GPIO 2

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASS)
        while not wlan.isconnected():
            time.sleep(0.5)
    print("WiFi Connected! IP:", wlan.ifconfig()[0])

def mqtt_callback(topic, msg):
    print(f"New message on {topic}: {msg}")
    if topic == TOPIC_SET_LED:
        if msg == b"ON":
            led.value(1)
            client.publish(TOPIC_STATE_LED, b"ON", retain=True)
        elif msg == b"OFF":
            led.value(0)
            client.publish(TOPIC_STATE_LED, b"OFF", retain=True)

# חיבור
connect_wifi()
client = MQTTClient(CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASS, keepalive=60)
client.set_callback(mqtt_callback)
client.connect()
client.subscribe(TOPIC_SET_LED)
print("MQTT Connected and subscribed!")

# לולאת ריצה ראשית
last_send = time.time()
simulated_temp = 24.0

while True:
    try:
        # בדיקה להודעות נכנסות מ-Home Assistant
        client.check_msg()

        # שידור ערך חיישן כל 10 שניות
        if time.time() - last_send > 10:
            client.publish(TOPIC_SENSOR, str(simulated_temp))
            last_send = time.time()

        time.sleep(0.1)
    except Exception as e:
        print("Connection lost, reconnecting...", e)
        time.sleep(5)
        client.connect()
        client.subscribe(TOPIC_SET_LED)