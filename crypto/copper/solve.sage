#!/usr/bin/env sage

from Crypto.Util.number import *

e = 3
exec(open("output.txt").read())

pad = bytes_to_long(bytes.fromhex(leak)) << 8 * 42

R = Zmod(N);
Rx.<x> = R['x']
p = (x + pad)**3 - c

roots = p.small_roots()
assert(len(roots) == 1)
m = roots[0]

print(long_to_bytes(m).decode())
