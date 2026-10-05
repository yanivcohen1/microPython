import time

# --- זיהוי סביבה ואתחול ספריות ---
emulator = False
try:
    import network
    from umqtt.simple import MQTTClient
    from machine import Pin, ADC
except ImportError:
    import paho.mqtt.client as paho_mqtt
    from machine import Pin, ADC
    emulator = True

try:
    from user_lib.settings import readEnvData
    env_data = readEnvData()
    WIFI_SSID = env_data.get("wifi_name", "")
    WIFI_PASS = env_data.get("wifi_pass", "")
except ImportError:
    WIFI_SSID = "YOUR_WIFI_SSID"
    WIFI_PASS = "YOUR_WIFI_PASSWORD"

# --- הגדרות MQTT ---
MQTT_BROKER = "192.168.0.103"
MQTT_USER = "esp32"
MQTT_PASS = "MyEspPass123!"
CLIENT_ID = "esp32_livingroom"

TOPIC_STATE_LED = "home/esp32/led/state"
TOPIC_SET_LED = "home/esp32/led/set"
TOPIC_SENSOR = "home/esp32/sensor/temp"

# --- אתחול חומרה ---
led = Pin(2, Pin.OUT)
led.value(1)  # אתחול ה-LED למצב כבוי
sliderPot = ADC(Pin(34))
sliderPot.atten(ADC.ATTN_11DB)

# --- חיבור WiFi (רק ב-ESP32) ---
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASS)
        while not wlan.isconnected():
            time.sleep(0.5)
    print("WiFi Connected! IP:", wlan.ifconfig()[0])

# --- לוגיקת בקרה משותפת להודעות ---
def handle_incoming_message(topic, payload_str, publish_func):
    print(f"New message on {topic}: {payload_str}")
    if topic == TOPIC_SET_LED:
        if payload_str == "ON":
            print(">> LED turned ON")
            led.value(0)  # או led.off() בהתאם ללוגיקת הלוח (Active Low / High)
            publish_func(TOPIC_STATE_LED, "ON", retain=True)
        elif payload_str == "OFF":
            print(">> LED turned OFF")
            led.value(1)
            publish_func(TOPIC_STATE_LED, "OFF", retain=True)

# --- אתחול והפעלת הלקוח ---
if emulator:
    print("Running in Simulator / Windows mode...")
    
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            client.subscribe(TOPIC_SET_LED)
        else:
            print(f"Failed to connect, return code {rc}")

    def on_message(client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode()
        handle_incoming_message(topic, payload, lambda t, p, retain=False: client.publish(t, p, retain=retain))

    client = paho_mqtt.Client(client_id=CLIENT_ID + "_sim")
    client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, 1883, 60)
    client.loop_start()

else:
    print("Running in ESP32 / MicroPython mode...")
    connect_wifi()

    def micropython_callback(topic, msg):
        t = topic.decode()
        p = msg.decode()
        handle_incoming_message(t, p, lambda top, pay, retain=False: client.publish(top.encode(), pay.encode(), retain=retain))

    client = MQTTClient(CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASS, keepalive=60)
    client.set_callback(micropython_callback)
    client.connect()
    client.subscribe(TOPIC_SET_LED.encode())
    print("Connected to MQTT Broker and subscribed!")

# --- לולאה ראשית ---
last_send = 0

try:
    while True:
        # ב-MicroPython יש לבדוק הודעות באופן יזום
        if not emulator:
            try:
                client.check_msg()
            except OSError:
                pass  # התעלמות משגיאות non-blocking אם אין הודעה ממתינה

        # קריאת החיישן ושידור פעם ב-2 שניות
        if time.time() - last_send >= 2:
            raw_val = sliderPot.read()
            slider_val = str(int(raw_val * 100 / 4095))
            
            if emulator:
                client.publish(TOPIC_SENSOR, slider_val)
            else:
                client.publish(TOPIC_SENSOR.encode(), slider_val.encode())
                
            print(f"Published sensor value: {slider_val}")
            last_send = time.time()

        time.sleep(0.1)

except KeyboardInterrupt:
    if emulator:
        client.loop_stop()
        client.disconnect()
    else:
        client.disconnect()
    print("Stopped.")