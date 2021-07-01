import socket
import base64
import os
import time

def listener():

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('127.0.0.1', 1338))
    s.listen(5)
    flag = b'(3,66827439388718004166721471471671102060)'
    while 1 == 1:

      cli, addr = s.accept()

      cli.send(b"Flag for you\n")
      cli.send(flag)
      # user = str(cli.recv(256), 'ascii')

      cli.close()


while 1 == 1:
  try:
    listener()
  except:
    time.sleep()
    continue
