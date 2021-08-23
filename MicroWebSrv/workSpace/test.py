# run os list
# import os
# print("os List:")
# print (os.listdir())
import user_lib.settings as settings
import datetime
  
# using now() to get current time
current_time = datetime.datetime.now()

print(current_time)
import os
cwd = os.getcwd()
print(cwd)

settings.appendLineToLogFile(str(current_time))


