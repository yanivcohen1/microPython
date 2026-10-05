# יצירת הסביבה (באמצעות ה-Python Launcher המפנה לגרסה 3.9)
py -3.9 -m venv venv

# הפעלת הסביבה ב-PowerShell
.\venv\Scripts\Activate.ps1
# (או ב-CMD: .\venv\Scripts\activate.bat)

# התקנת החבילה
pip install pyserial
pip install paho-mqtt
pip install esptool
python -m pip install rshell==0.0.30

# the file configuration.yaml location
/homeassistant/configuration.yaml

# ping -4 homeassistant.local
MQTT_BROKER = "192.168.0.103"

# rshell
rshell --buffer-size=30 -p COM3
cp ./settings.py /pyboard/

# start py shell and start the program
repl
import start.py
