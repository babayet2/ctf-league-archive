from binascii import hexlify
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import shamir
import os
import sys
import base64
import pandas as pd


shares = pd.read_csv("shares.csv", header=None).to_numpy()
shares = [(int(x[0]),int(x[1])) for x in shares]
secret = shamir.recover_secret(shares)

with open("flag.enc", "rb") as fi:
  enc = base64.b64decode(fi.read())
  iv = enc[0:16]
  enc = enc[16:]


  k = bytes(str(secret)[:32],'ascii')
  Cip = AES.new(k, AES.MODE_CBC, iv)
  print(secret)
  print(str(Cip.decrypt(enc), 'ascii').strip("\n"))
