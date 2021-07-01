#!/usr/bin/env python3

import ast
import socket
import threading
import sys

from common import *
from zkp import *

class Server:
    def __init__(self, ident, host='0.0.0.0', port=None):
        if port == None:
            port = int(trustee_hostports[ident][1])

        print(f"Binding to {host}:{port}")
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((host, port))

        self.ident = ident
        self.election_ids = set()
        self.election_ids_lock = threading.Lock()

        with open('data/flag' + str(ident), 'rb') as f:
            self.flag_share = f.read()
        with open('data/public_key', 'r') as f:
            self.N = int(f.read())
        with open('data/private_key' + str(ident), 'r') as f:
            self.d_share = int(f.read())

    def listen(self):
        self.s.listen(5)
        while True:
            c, addr = self.s.accept()
            threading.Thread(target=self.election, args=(c,)).start()

    def election(self, c):
        c.settimeout(5)
        f = c.makefile('r')

        try:
            c.sendall(b"What is the election ID?\n")
            election_id = int(f.readline())

            self.election_ids_lock.acquire()
            if election_id in self.election_ids:
                self.election_ids_lock.release()
                c.sendall(("Election ID " + str(election_id) + " already used.\n").encode())
                raise Exception()
            else:
                self.election_ids.add(election_id)
            self.election_ids_lock.release()

            c.sendall(b"Collecting other votes ...\n")
            with socket.socket() as s2:
                s2.connect(lyells_bot_hostport)
                f2 = s2.makefile('r')

                s2.sendall(str(election_id).encode() + b'\n')
                enc_votes = decode_ints(f2.readline(), N_CANDIDATES)

            c.sendall(b"Done.\nPlease enter your vote.\n")
            enc_vote = decode_ints(f.readline(), N_CANDIDATES)

            zkp = setup_zkp(enc_vote, self.N)
            proof = ast.literal_eval(f.readline())
            zkp.verify(*proof)

            c.sendall(b"Tallying results...\n")
            dec_vote_shares = []
            for i in range(N_CANDIDATES):
                enc_votes[i] = (enc_votes[i] * enc_vote[i]) % self.N**2

                # We only have a share of d, but that's fine as the client will combine our
                # dec_vote_shares with the other trustees' shares.
                dec_vote_shares.append(paillier_decrypt_r(enc_votes[i], self.N, self.d_share))

            c.sendall(", ".join([str(x) for x in enc_votes]).encode() + b"\n")
            c.sendall(b"Decryption shares:\n")
            c.sendall(", ".join([str(x) for x in dec_vote_shares]).encode() + b"\n")

            c.sendall(b"Please send the product of the shares, so that I know who won.\n")
            dec_vote_r = decode_ints(f.readline(), N_CANDIDATES)

            votes = [paillier_decrypt_m_from_r(c, r, self.N) for c, r in zip(enc_votes, dec_vote_r)]

            if votes[1] > votes[0]:
                c.sendall(b"Holy shit, Stan won! I thought for sure that Lyell would come out on top.\n")
                c.sendall(self.flag_share.hex().encode() + b"\n")
            else:
                c.sendall(b"Looks like we're in for another year of Lyell's tyranny.\n")

        finally:
            f.close()
            c.shutdown(1)
            c.close()

if __name__ == '__main__':
    server = Server(int(sys.argv[1]))
    server.listen()
