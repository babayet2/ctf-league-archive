from functools import reduce
import secrets # Note: this is a standard python library, not some secret part of the challenge.
from itertools import zip_longest

trustee_hostports = [
    ('trustee0.ctf-league.osusec.org', 31327),
    ('trustee1.ctf-league.osusec.org', 31328),
    ('trustee2.ctf-league.osusec.org', 31329),
]
stans_bot_hostport = ('stans_bot', 31330)

N_SHARES = len(trustee_hostports)

candidates = [
    ("Lyell Read", "You get a shirt, you get a shirt, you get a shirt. Everybody gets a shirt!"),
    ("Stan Lyakhov", "First we'll figure out what to do, then we'll do it!"),
]
N_CANDIDATES = len(candidates)

KEY_BITS = 2048
KEY_BYTES = KEY_BITS // 8
SECURITY_PARAMETER = 128
SECURITY_PARAMETER_BYTES = SECURITY_PARAMETER // 8

def decode_ints(msg, expected):
    outputs = [int(x.strip()) for x in msg.split(",")]
    assert len(outputs) == expected
    return outputs

# Given one or more byte strings, outputs the xor of them all as a byte string.
def xor(*values):
    return bytes([reduce(lambda a, b: a ^ b, l) for l in zip_longest(*values)])

def paillier_encrypt(m, N):
    r = secrets.randbelow(N)
    c = (pow(r, N, N**2) * (1 + m * N)) % N**2
    return c, r

# Normally Paillier decrypts m directly, but we want to be able to prove that the decryption is
# correct, which requires finding r and then decrypting the message m.
# Using d, we can find c**d = (r**N * (1 + m*N))**d = r**(N*d) = r (mod N).
def paillier_decrypt_r(c, N, d):
    return pow(c, d, N)

# After computing r, we can decrypt the message by using c * r**-N = 1 + m*N (mod N**2)
def paillier_decrypt_m_from_r(c, r, N):
    m = (c * pow(r, -N, N**2)) % N**2

    if m % N != 1:
        raise Exception("r is wrong")

    return (m - 1) // N
