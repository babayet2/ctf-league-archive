import base64

with open("message_bytes", "rb") as b:
  message = b.read()

  for i in range(256):
    test = []
    for j in message[0:16]:
      test.append(i^j)
      
    print(i, " ", bytes(test))

  n = int(input("\nwhich one: "))
  real = []
  for i in message:
    real.append(i^n)

  x = str(bytes(real), 'ascii').split(":")
  print('User: ', x[1])
  print('SSH_KEY: \n', str(base64.b64decode(bytes(x[2],'ascii')), 'ascii'))
  print('FLAG: ', x[3])
