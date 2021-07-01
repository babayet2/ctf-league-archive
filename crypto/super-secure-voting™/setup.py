#!/usr/bin/env python3

import secrets # Note: this is a standard python library, not some secret part of the challenge.
from Crypto.Util.number import getPrime

import os

from common import *


# Try to create data directory
try:
    os.mkdir("data")
except FileExistsError:
    pass

with open('flag', 'rb') as f:
    flag = f.read().strip()

# Give out secret shares of the flag
flag_shares = [secrets.token_bytes(len(flag)) for i in range(N_SHARES - 1)]
flag_shares.append(xor(*flag_shares, flag))

for i in range(N_SHARES):
    with open('data/flag' + str(i), 'wb') as f:
        f.write(flag_shares[i])


# Generate the Paillier key and give out secret shares of the private key.

p = getPrime(KEY_BITS // 2)
q = getPrime(KEY_BITS // 2)
N = p * q

phi = (p - 1) * (q - 1)
d = pow(N, -1, phi)

d_shares = [secrets.randbits(KEY_BITS + SECURITY_PARAMETER) for i in range(N_SHARES - 1)]
d_shares.append(d - sum(d_shares))

with open('data/public_key', 'w') as f:
    f.write(str(N))


for i in range(N_SHARES):
    with open('data/private_key' + str(i), 'w') as f:
        f.write(str(d_shares[i]))
