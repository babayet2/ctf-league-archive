import socket
import base64
import os
import time

def fix():

  key = None
  with open("/root/listeners/key.priv","rb") as f:
      key = base64.b64encode(f.read())

  x = os.urandom(1)[0]
  s = b"HiHithereHiHi:frederick:" + key + b':(2,18929204079384858729365442326481389204)'
  fixed = []
  for i in s:
    fixed.append(x^i)

  fixed = base64.b64encode(bytes(fixed))
  return bytes(fixed)

def listener():

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('0.0.0.0', 1337))
    s.listen(5)
    while 1 == 1:

      cli, addr = s.accept()

      payload = fix()
      cli.send(b"SSH Backup service, Key requested... Implementing security... done... sending...\n")
      cli.send(payload + b'\n')
      cli.send(b"Goodbye\n")

      cli.close()

while 1 == 1:
  try:
    listener()
  except:
    time.sleep(30)
    continue
