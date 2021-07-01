#!/usr/bin/env python3

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

key = get_random_bytes(16)

with open('flag', 'rb') as f:
    flag = f.read().strip()

# Encrypt data in output feedback mode.
# https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Output_feedback_(OFB)
def encrypt(nonce, data):
    cipher = AES.new(key, AES.MODE_OFB, iv=nonce)
    return nonce + cipher.encrypt(data)

flag_nonce = get_random_bytes(16)
print("Encrypted flag: " + encrypt(flag_nonce, flag).hex())

print("Please run a chosen plaintext attack")

while True:
    message = bytes.fromhex(input("What message would you like to encrypt? "))
    nonce = bytes.fromhex(input("Nonce? "))
    print("Your message, encrypted: " + encrypt(nonce, message).hex())
