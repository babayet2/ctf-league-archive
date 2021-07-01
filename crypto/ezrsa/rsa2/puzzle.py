#!/usr/bin/env python3

from Crypto.Util.number import *
import secrets

e = 3

while True:
    p = getPrime(1024)
    q = getPrime(1024)

    if p % e != 1 and q % e != 1:
        break

N = p * q
print("N =", N)

with open("flag", "r") as f:
    flag = f.read().strip().encode()
assert(len(flag) == 85)

m = bytes_to_long(flag)
c = pow(m, e, N)
print("c =", c)
