import binascii

bin_res = bin(int(binascii.hexlify(b'hello'), 16))
print(bin_res) # '0b110100001100101011011000110110001101111'
n = int(bin_res, 2)
str_res = binascii.unhexlify('%x' % n).decode("utf-8")
print(str_res)