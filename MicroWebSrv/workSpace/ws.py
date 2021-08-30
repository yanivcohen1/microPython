import os
try:
    os.remove("machine.py")
except :
    pass
    # print ("machine not exist")
print (os.listdir())
from user_lib.net import wifi_connect
wifi_connect()

import main_start_ws