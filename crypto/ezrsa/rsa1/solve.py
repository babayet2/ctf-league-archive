#!/usr/bin/env python3

from Crypto.Util.number import *

e = 3
exec(open("output.txt").read())

phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)

m = pow(c, d, N)
print(long_to_bytes(m))
