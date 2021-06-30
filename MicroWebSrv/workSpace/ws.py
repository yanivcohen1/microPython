import os
try:
    os.remove("machine.py")
except :
    pass
    # print ("machine not exist")
print (os.listdir())
import ynet
import main_start_ws