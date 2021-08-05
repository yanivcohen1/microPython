

def mapInRangToOutRang(val_in, in_min, in_max, out_min, out_max):
    return in_min + (((in_max - in_min)/(out_max - out_min))(val_in - out_min))