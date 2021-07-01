#!/usr/bin/env python3

import signal
import socket
import threading
from numpy.random import binomial

from common import *

MAX_OLD_VOTES = 1000

class Server:
    def __init__(self, host="0.0.0.0", port=lyells_bot_hostport[1]):
        print(f"Binding to {host}:{port}")
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((host, port))

        self.enc_votes = {}
        self.enc_votes_lock = threading.Lock()

        with open('data/public_key', 'r') as f:
            self.N = int(f.read())

    def listen(self):
        self.s.listen(5)
        while True:
            c, addr = self.s.accept()
            threading.Thread(target=self.vote, args=(c,)).start()

    def get_votes(self, election_id):
        if election_id in self.enc_votes:
            return self.enc_votes[election_id]

        self.enc_votes_lock.acquire()
        if election_id in self.enc_votes:
            self.enc_votes_lock.release()
            return self.enc_votes[election_id]

        # Give Stan 20% of the vote, so it doesn't look too suspicious.
        total_votes = 30
        vote_prob = 0.2
        votes = [0 for i in range(N_CANDIDATES)]

        # Make extra sure that Stan can't win.
        while True:
            votes[1] = binomial(total_votes, vote_prob)
            if votes[1] <= 14:
                break

        votes[0] = total_votes - votes[1]
        enc_votes = [paillier_encrypt(v, self.N)[0] for v in votes]
        self.enc_votes[election_id] = enc_votes

        if len(self.enc_votes) > MAX_OLD_VOTES:
            # Delete oldest encrypted votes.
            del self.enc_votes[next(iter(self.enc_votes))]
        self.enc_votes_lock.release()
        return enc_votes

    def vote(self, c):
        c.settimeout(5)
        f = c.makefile('r')

        try:
            election_id = int(f.readline())
            enc_votes = self.get_votes(election_id)
            c.sendall(", ".join([str(x) for x in enc_votes]).encode() + b"\n")

        finally:
            f.close()
            c.shutdown(1)
            c.close()

if __name__ == '__main__':
    server = Server()
    server.listen()
