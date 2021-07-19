import ucryptolib

def encrypt(str):
    enc = ucryptolib.aes(b'1234567890123456', 1)
    data_bytes = str.encode()
    encrypt_res = enc.encrypt(data_bytes + b'\x00' * ((16 - (len(data_bytes) % 16)) % 16))
    return encrypt_res

def decrypt(encrypt_str):
    dec = ucryptolib.aes(b'1234567890123456', 1)
    decrypt_res = dec.decrypt(encrypt_str) # b'input plaintext\x00'
    str_res = decrypt_res.decode("utf-8")
    return str_res

# inc_res = encrypt('str to encript')
# print(inc_res)
# dec_res = decrypt(inc_res)
# print(dec_res)
