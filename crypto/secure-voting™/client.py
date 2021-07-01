#!/usr/bin/env python3

import secrets # Note: this is a standard python library, not some secret part of the challenge.
import socket

from common import *
from zkp import *

# Make the connection transparent to the user.
def recvline(s):
    msg = s[1].readline()
    print(msg, end="")
    return msg

def sendline(s, msg):
    print(msg)
    s[0].sendall((msg + '\n').encode())

with open('data/public_key', 'r') as f:
    N = int(f.read())

election_id = secrets.randbits(128)
print(f"OSUSEC Presidential Election #{election_id}")

print("Candidates:")
for i, (name, slogan) in enumerate(candidates):
    print(f'{i}.\t{name:>16}: "{slogan}"')

print("\nEnter the number of the candidate you wish to vote for (or -1 for nobody):")
choice = int(input())

enc_vote = []
witnesses = []
prod_r = 1
for i in range(N_CANDIDATES):
    count = 1 if i == choice else 0
    if(i == 0):
        c, r = paillier_encrypt(count, N)
    else:
        c, r = paillier_encrypt(1000, N)
    enc_vote.append(c)
    witnesses.append((count, r))
    prod_r = (prod_r * r) % N

witnesses.append(((1 if 0 <= choice < N_CANDIDATES else 0), prod_r))

class ForgedProof(DecryptionProof):

zkp = setup_zkp(enc_vote, N)
proof = zkp.prove(witnesses)

print("Ballot encrypted, submitting to trustee servers ...\n")

sockets = []
for host, port in trustee_hostports:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    sockets.append((s, s.makefile('r')))

for s in sockets:
    assert("election ID?" in recvline(s))
    sendline(s, str(election_id))

for s in sockets:
    while "enter your vote." not in recvline(s):
        pass
    sendline(s, ", ".join([str(x) for x in enc_vote]))
    sendline(s, str(proof))

enc_votes = []
dec_vote_shares = []
for i, s in enumerate(sockets):
    assert "Tallying results..." in recvline(s)
    enc_votes.append(decode_ints(recvline(s), N_CANDIDATES))
    assert "Decryption shares:" in recvline(s)
    dec_vote_shares.append(decode_ints(recvline(s), N_CANDIDATES))

# All trustees should have the same set of encrypted votes.
for e in enc_votes:
    assert enc_votes[0] == e
enc_votes = enc_votes[0]

dec_vote_r = N_CANDIDATES * [1]
for trustee_shares in dec_vote_shares:
    for i, share in enumerate(trustee_shares):
        dec_vote_r[i] = (dec_vote_r[i] * share) % N

votes = [paillier_decrypt_m_from_r(c, r, N) for c, r in zip(enc_votes, dec_vote_r)]

print("\nElection Results:")
for (name, slogan), v in zip(candidates, votes):
    print(f"{name:>16}: {v}")
print("")

for s in sockets:
    recvline(s)
    sendline(s, ", ".join([str(r) for r in dec_vote_r]))

for s in sockets:
    print(s[1].read(), end="")
