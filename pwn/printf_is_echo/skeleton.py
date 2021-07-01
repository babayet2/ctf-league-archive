from pwn import *

#set the arch of the binary, this can be used internally by pwntools
context.arch = 'amd64'

#process or remote listener that we will communicate with
#p = process("name_of_binary")
#p = remote("address", port)

#https://docs.pwntools.com/en/stable/shellcraft.html
print("lets see some shellcode")
print(pwnlib.shellcraft.amd64.linux.sh())
