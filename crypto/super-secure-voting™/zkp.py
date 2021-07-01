from abc import ABC, abstractmethod
import hashlib
from itertools import zip_longest # Disallow zip(self.protocols, []) cheese.

from common import *

# Zero knowledge proofs (ZKPs) allow the prover to convince the verifier of some fact, without the
# prover revealing the witness, which is some information that establishes the truth of the fact.
# Essentially, ZKPs are cryptographic witness protection protocols. For voting, this will check that
# the voter didn't attempt to vote multiple times, or a negative number of times. We use a
# particular sort of ZKP called a Σ-protocol, which has three parts.
#
#     Prover                            Verifier
#                       msg1
#                     ------->
#
#                       chal
#                     <-------
#
#                       msg2
#                     ------->
#
# The prover first sends msg1, which commits it to some secrets that will be used to keep its
# witness in hiding. The verifier then selects a random challenge chal, which the prover must then
# solve using msg2.
#
# Stealing a metaphor from https://en.wikipedia.org/wiki/Zero-knowledge_proof#The_Ali_Baba_cave ,
# imagine that there is a vast cave system, with a very large number of tunnels, and that it is
# known that either all of the tunnels are connected to each other or they are all disconnected. The
# prover wants to convince the verifier that every entrance to the cave system is connected to every
# other. The prover first enters a random entrance in secret, which corresponds to sending msg1 in
# the Σ-protocol. The verifier then randomly chooses a cave exit and asks the prover to leave the
# cave system using that exit (equivalent to chal). If the prover does in fact exit from that cave
# (equivalent to msg2) then the verifier can be quite sure that the caves are connected, because the
# only other possibility is that the prover just happened to choose exactly the same cave entrance
# in the first phase. However, the prover has not revealed anything about the witness to the
# verifier by doing this proof. In fact, anybody could fake the information available to the
# verifier (msg1, chal, msg2), which is called the transcript, whether the caves are connected or
# not. They could randomly pick chal first, and then just have the prover enter (msg1) and exit
# (msg2) through the corresponding cave entrance. This means that the zero knowledge proof is only
# convincing to someone who chose chal themself.
#
# In this implementation, we use the Fiat-Shamir heuristic, which avoids the interaction between the
# prover and the verifier. Instead, chal is picked as the hash of the statement to be proved and of
# msg1, which ensures that the prover cannot know which cave (chal) the hash will select until after
# picking a cave to enter (msg1). We assume a special kind of Σ-protocol where chal and msg2
# uniquely determine the only msg2 that the verifier would accept. This allows the prover to just
# send (chal, msg2), and the verifier can find msg1 and check that its hash is chal.
#
# Chapter 6 of "Efficient Secure Two-Party Protocols" contains details on how Σ-protocols work.

# An instantiation represents a Σ-protocol proving some fact. The verifier's chosen chal is always
# assumed to be a 2 * SECURITY_PARAMETER bit number.
class SigmaProtocol(ABC):
    # The prover half of the Σ-protocol, proving a statement given a witness that shows that it is
    # true. First generate msg1 with first_msg, then respond to the verifier's challenge with
    # second_msg.
    @abstractmethod
    def first_msg(self, witness):
        pass
    @abstractmethod
    def second_msg(self, chal):
        pass

    # For any chal and msg2 there must be only a single possible msg1 that would make the verifier
    # accept the proof. Find this msg1.
    @abstractmethod
    def consistent_first_msg(self, chal, msg2):
        pass

    # Hash the statement being proved together with msg1 using the hashing algorithm hasher. This is
    # used to generate chal when using the Fiat-Shamir heuristic.
    @abstractmethod
    def hash_first_msg(self, msg1, hasher):
        pass

    # As part of generating a fake transcript of the protocol, sample a fake msg2 based on a
    # challenge. msg1 is not known yet, as it will be chosen using pick_chal. The msg2s generated
    # this way must look the same as those generated by second_msg.
    @abstractmethod
    def fake_second_msg(self, chal):
        pass

    # Sample chal randomly as a 2 * SECURITY_PARAMETER bit number, instead of using a hash function.
    @staticmethod
    def sample_chal():
        return secrets.randbits(2 * SECURITY_PARAMETER)

    # Use hash_first_msg to get chal from a hash function. This is the Fiat-Shamir heuristic.
    def pick_chal(self, msg1):
        hasher = hashlib.sha256()
        self.hash_first_msg(msg1, hasher)
        chal_bytes = hasher.digest()
        assert len(chal_bytes) == 2 * SECURITY_PARAMETER_BYTES
        return int.from_bytes(chal_bytes, byteorder='little')

    # Generate an honest proof of a true fact, using Fiat-Shamir.
    def prove(self, witness):
        msg1 = self.first_msg(witness)
        chal = self.pick_chal(msg1)
        msg2 = self.second_msg(chal)
        return (chal, msg2)

    # Verify the Fiat-Shamir zero knowledge proof.
    def verify(self, chal, msg2):
        msg1 = self.consistent_first_msg(chal, msg2)
        assert(chal == self.pick_chal(msg1))

    # Generate a fake transcript by sampling chal first, then sampling msg2 and finding the matching
    # msg1. This must look identical to honestly generated proofs.
    def fake_transcript(self):
        chal = self.sample_chal()
        msg2 = self.fake_second_msg(chal)
        msg1 = self.consistent_first_msg(chal, msg2)
        return (msg1, chal, msg2)

# Σ-protocol for proving that a ciphertext decrypts to a particular message. That is, for proving
# that c = witness**N * (1 + m*N) (mod N**2). This is from the "Protocol for n^s’th powers" on page
# 20 of "A Generalization of Paillier’s Public-Key System with Applications to Electronic Voting".
class DecryptionProof(SigmaProtocol):
    def __init__(self, m, c, N):
        # Instead of proving that c is an encryption of m, equivalently prove that c * (1 - m*N) is
        # an encryption of zero.
        self.c = (c * (1 - m * N)) % N**2
        self.N = N

    def first_msg(self, witness):
        self.witness = witness
        self.u = secrets.randbelow(self.N)
        return pow(self.u, self.N, self.N**2)

    def second_msg(self, chal):
        return (pow(self.witness, chal, self.N) * self.u) % self.N

    def consistent_first_msg(self, chal, msg2):
        assert(msg2 % self.N != 0)
        return (pow(msg2, self.N, self.N**2) * pow(self.c, -chal, self.N**2)) % self.N**2

    def hash_first_msg(self, msg1, hasher):
        hasher.update(msg1.to_bytes(2 * KEY_BYTES, byteorder='little'))

    def fake_second_msg(self, chal):
        return secrets.randbelow(self.N)

# Given a Σ-protocol proving a fact A, and another proving B, we can prove both A and B by running
# the two Σ-protocols in parallel. The same chal can be reused for both protocols because it only
# matters that chal is unpredictable when msg1 was chosen. One reference for this protocol is page
# 158 of "Efficient Secure Two-Party Protocols", although it doesn't give any details.
class AndProof(SigmaProtocol):
    def __init__(self, *protocols):
        self.protocols = list(protocols)

    # Basically just delegate to the protocols, except that the challenge is shared.

    def first_msg(self, witness):
        return [p.first_msg(w) for p, w in zip_longest(self.protocols, witness)]

    def second_msg(self, chal):
        return [p.second_msg(chal) for p in self.protocols]

    def consistent_first_msg(self, chal, msg2):
        return [p.consistent_first_msg(chal, m2) for p, m2 in zip_longest(self.protocols, msg2)]

    def hash_first_msg(self, msg1, hasher):
        for p, m1 in zip_longest(self.protocols, msg1):
            p.hash_first_msg(m1, hasher)

    def fake_second_msg(self, chal):
        return [p.fake_second_msg(chal) for p in self.protocols]

# Given a Σ-protocol proving a fact A, and another proving B, prove that either A or B is true.
# This is a little more complicated than AndProof. The main idea is to give the prover the power
# to make one of its proofs a fake, then have it produce proofs of both statements. Specifically,
# instead of the overall chal being the challenge for both A and B, it will be the xor of the two
# challenges. The prover can pick only one of the two challenges in advance, and the other will be
# determined by the xor.
#
# This is described in more detail in Protocol 6.4.1 of "Efficient Secure Two-Party Protocols".
class OrProof(SigmaProtocol):
    def __init__(self, protocol0, protocol1):
        self.protocols = [protocol0, protocol1]

    def first_msg(self, witness):
        true_case, witness = witness
        self.true_case = true_case
        self.fake = self.protocols[1 - true_case].fake_transcript()

        msg1 = 2 * [None]
        msg1[true_case] = self.protocols[true_case].first_msg(witness)
        msg1[1 - true_case] = self.fake[0]
        return msg1

    def second_msg(self, chal):
        msg2s = 2 * [None]
        msg2s[self.true_case] = self.protocols[self.true_case].second_msg(chal ^ self.fake[1])
        msg2s[1 - self.true_case] = self.fake[2]

        chal0 = self.fake[1] ^ ((1 - self.true_case) * chal)
        return [chal0] + msg2s

    def consistent_first_msg(self, chal, msg2):
        chal0 = msg2[0]
        msg2s = msg2[1:]
        chals = [chal0, chal0 ^ chal]
        return [p.consistent_first_msg(c, m2) for p, c, m2 in zip_longest(self.protocols, chals, msg2s)]

    def hash_first_msg(self, msg1, hasher):
        for p, m1 in zip_longest(self.protocols, msg1):
            p.hash_first_msg(m1, hasher)

    def fake_second_msg(self, chal):
        chal0 = SigmaProtocol.sample_chal()
        return [chal0] + [p.fake_second_msg(c) for p, c in zip_longest(self.protocols, chal)]

# Return a Σ-protocol to prove that the encrypted vote was constructed properly. That is, that every
# candidate received either 0 or 1 votes, and that either 0 or 1 candidates received a vote.
def setup_zkp(enc_vote, N):
    zero_or_one_proofs = [OrProof(
        DecryptionProof(0, c, N),
        DecryptionProof(1, c, N)) for c in enc_vote]

    # Also check that there was at most 1 vote across all candidates.
    enc_vote_all_candidates = 1
    for c in enc_vote:
        enc_vote_all_candidates = (enc_vote_all_candidates * c) % N**2

    zero_or_one_proofs.append(OrProof(
        DecryptionProof(0, enc_vote_all_candidates, N),
        DecryptionProof(1, enc_vote_all_candidates, N)))

    zkp = AndProof(*zero_or_one_proofs)
    return zkp
