simulation = False
import json
# import settings
try:
    import network
except:
    simulation = True
    from pathlib import Path

def saveToDataFile(data):
    with open('data.txt', 'w') as f: # "a"-for Append, 'w'=for Overwrite
        f.write(data)

def readFromDataFile():
    with open('data.txt', 'r') as f:
        data = f.read()
    return data

def isEmulated():
    return env_data["emulated"]

def readEnvData():
    return env_data

def readFromFile(name):
    with open(name, 'r') as f:
        data = f.read()
    return data

def saveOveriteLogFile(data):
    with open('log.txt', 'w') as f: # "a"-for Append, 'w'=for Overwrite
        f.write(data)

def appendLineToLogFile(line):
    # append file
    file_a = open("log.txt","a")
    file_a.write(line)
    file_a.write('\n')
    file_a.close()
    # check size
    fin = open("log.txt","r")
    data = fin.read().splitlines(True)
    fin.close()
    # file limit
    if len(data) > 120:
        fout = open("log.txt","w")
        for line in data[20:]:
            fout.write(line)
        fout.close()

    # with open('workSpace\log.txt', 'r') as fin:
    #     data = fin.read().splitlines(True)
    # with open('workSpace\log.txt', 'w') as fout:
    #     if len(data) > 100:
    #         fout.writelines(data[1:])
    # with open('workSpace\log.txt', 'a') as file: # "a"-for Append, 'w'=for Overwrite
    #     file.write(line + "\n")
    
def readLinesFromLogFile():
    lines = None
    with open('log.txt', 'r') as file:
        lines = file.readlines()
    return lines

env_file = "env.json"
if simulation:
    script_dir = Path(__file__).parent.parent
    env_file = script_dir / "env.json"
json_data = readFromFile(env_file) # {"wifi_name": "TP-Link_F34F_5G", "wifi_pass": "73769835"}
env_data = json.loads(json_data)
print("emulated:", env_data["emulated"])

# insted of:
# f = open('data.txt', 'w')
# f.write('some test data')
# f.close()
# # read it
# f1 = open('data.txt')
# f1.read()
# f1.close()
# =============================================================================