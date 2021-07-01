#!/usr/bin/env python3

from Crypto.Util.number import *
import gmpy2

e = 3
exec(open("output.txt").read())

m = int(gmpy2.iroot(c, 3)[0])
print(long_to_bytes(m))
