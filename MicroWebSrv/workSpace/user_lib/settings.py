def saveToDataFile(data):
    with open('data.txt', 'w') as f: # "a"-for Append, 'w'=for Overwrite
        f.write(data)

def readFromDataFile():
    with open('data.txt', 'r') as f:
        data = f.read()
    return data