

def mapInRangToOutRang(val_in, in_min, in_max, out_min, out_max):
    return out_min + (((out_max - out_min) / (in_max - in_min)) * (val_in - in_min))

# test
# print(mapInRangToOutRang(2,1,3,2,4)) # need to be 3
# print(mapInRangToOutRang(2,1,3,2,6)) # need to be 4