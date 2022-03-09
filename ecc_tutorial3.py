# elliptic curve cryptography tutorial/playground (part 3)

from dumb25519 import Scalar, Point
import dumb25519

# unlike part 1 and part 2 tutorials, this tutorial is not much about
# the elliptic curve stuff. instead, this is about proving systems.
# proving systems involves two characters: Prover and Verifier.
# Prover has a secret and he must convince the Verifier about facts
# regarding the secret, WITHOUT revealing the secret.

# there are two "versions" of proving systems: interactive and non-interactive.
# in the interactive version, Verifier is involved *during* the creation of
# full proof by Prover. in cryptography papers, it is the interactive version
# that is usually presented. on the other hand, in the non-interactive version,
# the full proof is created by Prover alone, and Verifier will only verify
# the full proof. in actual implementations of cryptography, it is the
# non-interactive version that is usually implemented. we'll cover both here.

# exercise: implement Schnorr protocol
# read more: https://en.wikipedia.org/wiki/Proof_of_knowledge#Schnorr_protocol
# note: the wiki uses "multiplicative notation" for the group binary operation
# (more common overall), but these tutorials (and Monero resources) use
# "additive notation" (more commonly seen when dealing with elliptic curves).
#
# Schnorr protocol is among the simplest proving system currently used!
#
# here's the scenario:
#     Prover has a secret scalar x. he sends the commitment P = xG to Verifier.
#     by the Discrete Logarithm (DL) assumption (see part 1), Verifier will not
#     be able to crack the value of x. however the Verifier still wants to be
#     convinced that the Prover really knows x. how would the Prover do that?
# Schnorr protocol allows Prover to do this!

# interactive
class SchnorrProof:
    def __init__(self, x: Scalar, P: Point):
        # we'll not store the secret x here.
        self.P = P
        # let r be a random scalar (don't put in self). let self.Q = rG.
        # <your code here>

        # now Prover would send P and Q to Verifier.
        # like in previous tutorial parts, just imagine.

        # once Verifier received P and Q, she gives an
        # interactive challenge c to Prover.
        self.c = dumb25519.random_scalar()

        # once Prover received the challenge c, let self.s = r + c * x.
        # <your code here>

        # now Prover would send s to Verifier. this completes the full proof.

    def verify(self) -> bool:   # don't edit this line!
        # once Verifier receives the full proof, she can now verify it.
        # return s * G == Q + c * P
        # <your code here>
        pass

# non-interactive
class NISchnorrProof:
    def __init__(self, x: Scalar, P: Point):
        # we'll not store the secret x here.
        self.P = P
        # let r be a random scalar (don't put in self). let self.Q = rG.
        # <your code here>

        # unlike in interactive version, Prover must generate the challenge
        # himself. however, he should not be able to cheat by manipulating the
        # challenge. hence, the challenge instead should be the hash of the
        # partial proof data. this trick is called "Fiat-Shamir heuristic".
        c = dumb25519.hash_to_scalar("Schnorr Proof", self.P, self.Q)   # yeah, not in self!

        # let self.s = r + c * x.
        # <your code here>

        # now Prover would send the full proof (P, Q, s) to Verifier.

    def verify(self) -> bool:   # don't edit this line!
        # once Verifier receives the full proof, she can now verify it.
        # return s * G == Q + hash_to_scalar("Schnorr Proof", P, Q) * P
        # <your code here>
        pass

if __name__ == '__main__':
    # test 1 (should work)
    prvkey = dumb25519.random_scalar()
    pubkey = prvkey * dumb25519.G
    
    # Proof1 = SchnorrProof(prvkey, pubkey)   # also try NISchnorrProof
    # if Proof1.verify():
        # print("Verified!")
    # else:
        # print("Something's wrong :(")

    # test 2 (should NOT work)
    prvkey = dumb25519.random_scalar()
    pubkey = (prvkey + Scalar(1)) * dumb25519.G

    # Proof2 = SchnorrProof(prvkey, pubkey)   # also try NISchnorrProof
    # if Proof2.verify():
        # print("Something's wrong :(")
    # else:
        # print("Prover you're desperate!")
