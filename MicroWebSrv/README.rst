// https://www.wemos.cc/en/latest/d32/d32_pro.html
// by reading the cpu specification install the serial communication driver 
// for d32 spram bord install "CH341SER_WIN_3.5.zip"
// for the nospram bord install "CP210x_win_driver_esp32.zip"
// for testting python ident run
python -tt
Flaskr
======

The basic blog app built in the Flask `tutorial`_.

.. _tutorial: http://flask.pocoo.org/docs/tutorial/

To add dependencys lib in file "setup.py"in setup(install_requires=["dependencyslibName"])

Install
-------

**Be sure to use the same version of the code as the version of the docs
you're reading.** You probably want the latest tagged version, but the
default Git version is the master branch. ::

    # clone the repository
    $ git clone https://github.com/pallets/flask
    $ cd flask
    # checkout the correct version
    $ git tag  # shows the tagged versions
    $ git checkout latest-tag-found-above
    $ cd examples/tutorial

Create a virtualenv and activate it::

    $ python3 -m venv venv
    $ . venv/bin/activate

on linux use pip3 and python3

Add to windows path:
C:\Users\yaniv\anaconda3
C:\Users\yaniv\anaconda3\Scripts; 
C:\Users\yaniv\anaconda3\Library\bin 
//install
pip install virtualenv
//for anaconda3 open powerShell in admin and type:
Set-ExecutionPolicy RemoteSigned
// then "control"+"shift"+"p" and type "reload window"
**************************************************************

Or on Windows cmd::

    // needed python3.8 for rshell so for creating env you need python 3.8 for "python -m venv venv"
    $ py -m venv venv
    $ venv\Scripts\activate
    $ venv\Scripts\activate.bat
    $ python -m pip install --upgrade pip
    $ pip install esptool
    $ python -m pip install esptool==3.1
    $ esptool.py version
    ## test it
    $ esptool.py --chip esp32 --port COM6 flash_id
    $ esptool.py --chip esp32 --port com6 erase_flash
    $ esptool.py --chip esp32 --port com6 --baud 460800 write_flash -z 0x1000 "C:\Downloads\esp32-20210623-v1.16.bin"
    $ python -m pip install rshell==0.0.30
    $ rshell --editor nano --buffer-size=30 -p COM6
    $ rshell --buffer-size=30 -p COM7
    $ rsync ./workSpace  /pyboard
    $ rsync ./  /pyboard
    $ cp dir/file.py /pyboard/dir/
    $ repl
    >> import ws
    ## control + c to exit
    ## to run the code
    $ import ws
    ## control + c to stop the code
    ## control + x to exit repl

in PS for mobile simulation - need to be without envirment to use external py.exe 
    cd C:\Users\yaniv\OneDrive\microPython\MicroWebSrv\workSpace
    py .\main_start_ws.py

With PS:
cd C:\Users\yaniv\OneDrive\microPython\MicroWebSrv\
venv\Scripts\activate
rshell --buffer-size=30 -p COM6
rsync ./workSpace/  /pyboard
rsync ./  /pyboard
repl
## control + c to exit
## to run the code
>> import ws
## control + c to stop the code
## control + x to exit repl
*****************************************************

for REPL tester ( in event page )::

# read from other programs variables
global res
from ultrasonic_page import sliderIn
res = sliderIn

# read free RAM memory
import micropython, gc
gc.collect()
micropython.mem_info()

# read free flash memory
import uos
fs_stat = uos.statvfs('/')
fs_size = fs_stat[0] * fs_stat[2]
fs_free = fs_stat[0] * fs_stat[3]
print("File System Size {:,} - Free Space {:,}".format(fs_size, fs_free))

# read and set HW
# https://docs.micropython.org/en/latest/esp32/quickref.html
global res
from machine import Pin, ADC, Signal
from time import sleep

# led on and off
led_pin = Pin(0, Pin.OUT, Pin.PULL_UP, value=1) # set pin high on creation
# for inverting pin (true/false)
led = Signal(led_pin, invert=True)
led.on()
sleep(2)
led.off()

# 5v relay on esp32 pin 13
relay_pin = Pin(13, Pin.OUT)
relay = Signal(relay_pin, invert=True)
relay.on()
sleep(2)
relay.off()

# ADC read potentiometer
adc = ADC(Pin(34)) 
adc.atten(ADC.ATTN_11DB)    # set 11dB input attenuation (voltage range roughly 0.0v - 3.6v)
adc.width(ADC.WIDTH_12BIT)   # set 12 bit return values (returned range 0-4095)
res = int(adc.read() * 100 / 4095)

# DAC make sinus wave DAC pin-25
import math
import time
from machine import DAC, Pin
dac = DAC(Pin(25, Pin.OUT), bits=8)
buf = bytearray(255) # create a buffer containing a sine-wave
while True:
    for i in range(len(buf)):
        buf[i] = 128 + int(127 * math.sin(2 * math.pi * i / len(buf)))
        dac.write(buf[i])
        time.sleep(1/400) # 400Hz

# PWM dim buildin led pin-5
# PWM(Pin(5), freq=20000, duty=950) # duty is how mach off 1023 is on
from machine import Pin, PWM
from time import sleep
frequency = 5000
pwm_led = PWM(Pin(5), frequency)
while True:
  for duty_cycle in range(0, 1024):
    pwm_led.duty(duty_cycle)
    sleep(0.005)
# pwm_led.deinit() # free resource

# Time difrance calc - for simulation this is in machine
import time
start = time.ticks_ms() # get millisecond counter
delta = time.ticks_diff(time.ticks_ms(), start) # compute time difference

# timer number 0 - timers 0 to 3
from machine import Timer
tim0 = Timer(0)
tim0.init(period=5000, mode=Timer.ONE_SHOT, callback=lambda t:print(0)) # internal function
def cb_timer(time, someParameter): # timer callback function
    print(time)
cb = lambda timer: cb_timer(timer, someParameter)
timer0.init(period=1000, callback=cb) # defoult is mode=Timer.PERIODIC, The period is in milliseconds

# WDT (Watchdog timer) reset if program is stack
# application must “feed” the watchdog periodically
from machine import WDT
wdt = WDT(timeout=5000) # enable the WDT with a timeout of 5s (1s is the minimum)
wdt.feed() # need to call these two fun minimum evry 5s or the bord will restart itself

# read time from internet
from machine import RTC
rtc = RTC()
# synchronize with ntp
# need to be connected to wifi
import ntptime
ntptime.settime() # set the rtc datetime from the remote server
# get the date and time in UTC-Universal Time Coordinated
# for jerusalem need to add 3 to houre - (GMT/UTC)+3
year, monte, day, houre, mimite, secend, mi, n = rtc.datetime()    

# machine reset
machine.reset()

# read input by event on press (not on release)
btn = Pin(0, Pin.IN)
def blink_fun(pin):
    led.on() if btn()==1 else led.off()  
btn.irq(blink_fun)

# file list
import os
print (os.listdir())
***********************************************

Install Flaskr::

    $ pip install -e .
    #linux
    $pip install --user pipenv
    $pip install --user -e .

Or if you are using the master branch, install Flask from source before
installing Flaskr::

    $ pip install -e ../..
    $ pip install -e .


Run
---

on linux ::

    $ export FLASK_APP=flaskr
    $ export FLASK_ENV=development
    $ flask init-db
    $ flask run

on PS ::

    > $env:FLASK_APP = "flaskr"
    > $env:FLASK_ENV = "development"
    > flask init-db
    > flask run

    to run the angular server.py > $env:FLASK_APP = ".\flaskr\server.py"
    flask run
    yarn
    yarn start
    Open http://127.0.0.1:4200 in a browser.

Or on Windows cmd::

    cd .\flaskr\
    > set FLASK_APP=flaskr
    > set FLASK_ENV=development
    > flask init-db
    > flask run

//run the .\flaskr\app.py
Open http://127.0.0.1:5000 in a browser.
username: yaniv
pass: 1234

Debug in vsc
------------
run in debug window task: 'Python: Flask'
or
python -m debugpy --listen 5678 ./fileName.py
and run "Python: Attach"

Test
----

::

    $ pip install '.[test]'
    $ pytest

Run with coverage report::

    $ coverage run -m pytest
    $ coverage report
    $ coverage html  # open htmlcov/index.html in a browser

Deploy
------
https://flask.palletsprojects.com/en/1.1.x/tutorial/deploy/
https://github.com/pallets/flask/tree/master/examples/tutorial
python3 -m ensurepip --default-pip
python3 -m pip install --upgrade pip setuptools wheel
pip install wheel
//python setup.py sdist
python setup.py sdist bdist_wheel
this creacte a dist directory with two files theSourceCode.tar.gz & libs.whl

Run with a Production machine
-----------------------------
Create a virtualenv as above describe
pip install wheel
pip install flaskr-1.0.0-py3-none-any.whl
Run as above describe

Run as production server
------------------------
pip install waitress
pip install wheel
disable the firewall comodo
Create a virtualenv as above describe
Run as above describe without the development variable
waitress-serve --port=5000 --call 'flaskr:create_app'
// --call 'module:function'
// module is the file name.
// need to import the fileName from mainModule