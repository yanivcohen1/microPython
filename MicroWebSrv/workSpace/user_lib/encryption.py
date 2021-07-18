import binascii

def encrypt(str):
    bin_res = bin(int(binascii.hexlify(bytearray(str, "utf8")), 16))
    hex_res = hex(int(bin_res, 2))
    return hex_res # '0b110100001100101011011000110110001101111'

def dencrypt(str):
    to_bin = bin(int(str, 16))
    n = int(to_bin, 2)
    str_res = binascii.unhexlify('%x' % n).decode("utf-8")
    return str_res

# inc_res = incrapt('hi yaniv')
# print(inc_res)
# dec_res = descrapt(inc_res)
# print(dec_res)
