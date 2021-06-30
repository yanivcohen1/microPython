import os
try:
    os.remove("machine.py")
except :
    print ("machine not exist")
print (os.listdir())
import ynet
import main_start_ws