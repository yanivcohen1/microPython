import uos as os 
import machine

os.mount(machine.SDCard(), "/sd")   # load sd

print(os.listdir("/sd"))            #print the filename in '/sd' dir

f=open("sd/HelloWord.txt","w")      #open file 'HelloWord.txt' in sdcard 
f.write("HelloWord!!!")             #write "HelloWord!!!" to the file
f.close()                           #close file

f=open("sd/HelloWord.txt","r")      #open file 'HelloWord.txt' in sdcard 
print(f.read())                     #read data from file
f.close()

os.umount("/sd")                    # unload sd