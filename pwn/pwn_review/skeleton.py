from pwn import *

#set the arch of the binary, this can be used internally by pwntools
context.arch = 'amd64'

#process or remote listener that we will communicate with
#p = process("name_of_binary")
#p = remote("address", port)

#https://docs.pwntools.com/en/stable/shellcraft.html
print("lets see some shellcode")
print(pwnlib.shellcraft.amd64.linux.sh())
print("lets see some shellcode ready to be written as bytes")
print(asm(pwnlib.shellcraft.amd64.linux.sh()))

#send hello to a binary
#p.send("hello")

#receive everything the binary has sent back to the buffer
#p.recv()
#receive 8 bytes
#p.recv(8)

