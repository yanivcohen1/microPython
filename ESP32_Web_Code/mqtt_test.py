from micropython import const  # type: ignore
from machine import I2C, Pin, UART  # type: ignore
from onewire import OneWire, OneWireError  # type: ignore
from ds18x20 import DS18X20  # type: ignore
from ina219 import INA219
from logging import INFO
from settings import get_p2
from tracer import Tracer, TracerSerial, QueryCommand
from time import sleep
from ujson import dumps
from umqtt.simple import MQTTClient

# Configure MQTT client
client = MQTTClient(client_id="vegepod_client",
                    server="10.0.7.99",
                    port=1883,
                    user="mqtt",
                    password=get_p2())

# Sensor constants
EMPTY = const(0)
MID = const(1)
ERROR = const(2)
FULL = const(3)
CANOPY_ON = const(0)
CANOPY_OFF = const(1)

# Configure GPIO inputs
level_upper = Pin(14, Pin.IN, Pin.PULL_UP)
level_lower = Pin(12, Pin.IN, Pin.PULL_UP)
canopy_magnet = Pin(27, Pin.IN, Pin.PULL_UP)
extra1 = Pin(23, Pin.IN, Pin.PULL_UP)
extra2 = Pin(4, Pin.IN, Pin.PULL_UP)

# Configure INA219
SHUNT_OHMS = 0.1
i2c = I2C(0, scl=Pin(18), sda=Pin(19))
ina = INA219(SHUNT_OHMS,
             i2c,
             max_expected_amps=.04,
             log_level=INFO)
ina.configure(voltage_range=ina.RANGE_16V,
              gain=ina.GAIN_1_40MV,
              bus_adc=ina.ADC_128SAMP,
              shunt_adc=ina.ADC_128SAMP)
ina.sleep()

# Configure DS18B20
dat = Pin(5)
ds = DS18X20(OneWire(dat))
roms = ds.scan()  # scan for devices on the bus
print('found devices:', roms)

# Configure Tracer MPPT
port = UART(2, 9600, rx=13, tx=15)
tracer = Tracer(0x16)
t_ser = TracerSerial(tracer, port)
query = QueryCommand()
t_ser.flush()  # Clear any existing data on serial port


def get_data():
    try:
        t_ser.send_command(query)
        sleep(.2)
        if t_ser.port.any():
            data = t_ser.receive_result()
            if data is None:
                return('No data returned.')
        else:
            return('No data returned.')
        return data
    except (OSError) as e:
        return 'Error:' + str(e)


try:
    loop_time = 10  # 10 seconds
    while True:
        vegepod_data = {}

        # Temperature
        try:
            ds.convert_temp()
            sleep(.75)
            temp = ds.read_temp(roms[0])
            tempf = temp * 9/5.0 + 32  # Convert to fahrenheit
            if 0 <= tempf <= 125:  # Validate temperature range
                print('Temperature: {0:0.2f}°C, {1:0.2f}°F'.format(temp, tempf))
                vegepod_data["temperature"] = round(tempf, 1)
            else:
                print('Range Error: {0:0.2f}°C, {1:0.2f}°F'.format(temp, tempf))
        except OneWireError:
            print('Failed to read onewire sensor.')
        except RuntimeError as error:
            print("Onewire error" + error.args[0])
        except:
            print("Unknown onewire error.")

        # Wind Speed
        ina.wake()
        sleep(.3)  # Delay to ensure ina revived from sleep
        i = ina.current()
        ina.sleep()
        wind = (i - 4) * 1.3  # manual states 1.875, anemometer shows 1.3
        wind_kph = wind * 3.6
        wind_mph = round(wind * 2.237, 1)
        print("Wind Speed: {0:0.2f} m/s, {1:0.2f} km/h, {2:0.2f} mph".format(
              wind, wind_kph, wind_mph))
        vegepod_data["wind"] = wind_mph

        # Solar Power
        data = get_data()
        if type(data) is str:
            # Error
            print(data)
            t_ser.flush()
        else:
            print("Battery: {} V, PV: {} V, Charge: {} A, Load: {} A".format(
                data.batt_voltage,
                data.pv_voltage,
                data.charge_current,
                data.load_amps))
            vegepod_data["battery"] = data.batt_voltage
            vegepod_data["panel"] = data.pv_voltage
            vegepod_data["charging"] = data.charge_current * 1000
            vegepod_data["load"] = data.load_amps * 1000
            if isinstance(data.pv_voltage, (int, float)):
                if data.pv_voltage > 12:
                    # Set loop time to 10 seconds when solar above 12 V
                    loop_time = 10
                else:
                    # Set loop time to 10 minutes when solar drops
                    loop_time = 600
 
        # Water Level
        water_level = level_upper.value() << 1 | level_lower.value()
        level_msg = ""
        if water_level is EMPTY:
            level_msg = "Empty"
        elif water_level is MID:
            level_msg = "Midway"
        elif water_level is FULL:
            level_msg = "Full"
        else:
            level_msg = "Error"
        print("Water level: " + level_msg)
        vegepod_data["level"] = level_msg
        print(dumps(vegepod_data))
        
        # Canopy
        canopy_msg = ""
        if canopy_magnet.value() is CANOPY_ON:
            print('Canopy on.')
            canopy_msg = "ON"
        else:
            print('Canopy off.')
            canopy_msg = "OFF"

        # Publish MQTT sensor data
        try:
            client.connect()

            try:
                client.publish(b'homeassistant/sensor/vegepod/state',
                    dumps(vegepod_data))
                print("Published MQTT sensor data.")
                client.publish(b'homeassistant/binary_sensor/vegepod/state',
                    canopy_msg)
                print("Published MQTT binary sensor data.")
            except OSError:
                print("Failed to publish MQTT sensor data.")
            
            client.disconnect()
        except OSError:
            print("Failed to connect MQTT client.")

        print("Extra1: {}, Extra2: {}\n".format(extra1.value(), extra1.value()))

        sleep(loop_time)
except KeyboardInterrupt:
    print("\nCtrl-C pressed.  Cleaning up serial port and exiting...")
finally:
    port.deinit()


