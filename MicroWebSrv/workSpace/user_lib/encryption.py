import ucryptolib
import uhashlib

def encrypt(str):
    enc = ucryptolib.aes(b'1234567890123456', 1)
    data_bytes = str.encode("utf-8")
    encrypt_res = enc.encrypt(data_bytes + b'\x00' * ((16 - (len(data_bytes) % 16)) % 16))
    return encrypt_res

def decrypt(encrypt_bytes_res): # b'\xfe!F\x87?\xdb\x19\x18\xcdM\x83\x9b\xaa\x02\xa9\x04'
    dec = ucryptolib.aes(b'1234567890123456', 1)
    decrypt_res = dec.decrypt(encrypt_bytes_res)
    str_res = decrypt_res.decode("utf-8")
    return str_res

def sha256(str):  
    enc_bytes = str.encode("utf-8") # b"test"
    uhashlib.sha256(enc_bytes).digest()
    
# inc_res = encrypt('str to encript')
# print(inc_res)
# dec_res = decrypt(inc_res)
# print(dec_res)
