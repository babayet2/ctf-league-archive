from binascii import hexlify
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import shamir
import os
import sys
import base64




def get_shares():
  secret, shares = shamir.make_random_shares(8, 8)
  with open("shares.csv", "w") as f:
    for idx, share in shares:
      f.write( str(idx) + "," + str(share) + "\n")

  return secret, shares

def enc_flag(secret):
  with open("flag.txt", "r") as fi, open("flag.enc", "wb") as fo:
    iv = os.urandom(16)

    message = fi.read()
    #append timestamp to message
    #pad message with 0 bytes to match block size
    message = message + "\x00" * (16 - (len(message) % 16))
                       
    #Create AES object with key and iv
    k = bytes(str(secret)[:32], 'ascii')

    Cip = AES.new(k, AES.MODE_CBC, iv)
    text = Cip.encrypt(message)
 
    fo.write(base64.b64encode(iv + text) + b"\n")

if sys.argv[1] == "all":
  enc_flag(get_shares()[0])
elif sys.argv[1] == 'enc':
  enc_flag(int(sys.argv[2]))
