#!/usr/bin/env python3

from Crypto.Util.number import *
import secrets

e = 3

while True:
    p = getPrime(1024)
    q = getPrime(1024)

    if p % e != 1 and q % e != 1:
        break

print("p =", p)
print("q =", q)

N = p * q
print("N =", N)

with open("flag", "r") as f:
    flag = f.read().strip().encode()
assert(len(flag) == 37)

padding = secrets.token_bytes(250 - len(flag))

m = bytes_to_long(flag + padding)
c = pow(m, e, N)
print("c =", c)
