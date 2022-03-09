# elliptic curve cryptography tutorial/playground (part 1)

from dumb25519 import Scalar, Point
import dumb25519

# treat an elliptic curve group of points like you do vectors:
# you can add/subtract points (G + H, G - H) and you can do scalar
# multiplication with it (x * G or xG for short).
# ...and the analogy stops there.
#
# HOWEVER, we can have a vector/array OF scalars & OF points (part 2).

# difference #1: the scalars. in vector calculus, the scalar is real
# numbers. on the other hand, our scalar is integers modulo a large
# prime number l. in other words, our scalars are only from 0 to (l - 1)
# (the remainders when any integer is divided by l).
# Here's the l:
print("l = " + str(dumb25519.l))

# scalar initialize
one = Scalar(1)
two = Scalar(2)
sum = one + two

print("Addition:")
print(str(one) + " + " + str(two) + " = " + str(sum))
print("Woah! It's written differently. This is because relevant types of data have a standard \
format (it's in hex).")
print("Here's the more normal-looking equation:")
print(str(one.x) + " + " + str(two.x) + " = " + str(sum.x))

# other operations
diff = one - two
print(str(one.x) + " - " + str(two.x) + " = " + str(diff.x))
print("What?! Not -1? Again, our numbers are only from 0 to (l - 1). Hence -1 becomes \
\"the same\" with (l - 1).")

prod = one * two
print(str(one.x) + " * " + str(two.x) + " = " + str(prod.x))

# we have something like "division", but we do not use slash.
# instead, inversion (analogous to "reciprocal") is performed on the supposed
# divisor, then perform multiplication.
quot = one * two.invert()
print(str(one.x) + " / " + str(two.x) + " = " + str(quot.x))
print("...Yeah this doesn't make much sense. 1/2 becomes \"the same\" with... that quotient.\n\
To make sense of this, we multiply the \"quotient\" and 2. The product should be 1 \
like x * (1/x) = 1.")
prod2 = two * quot
print(str(two.x) + " * " + str(quot.x) + " = " + str(prod2.x) + " :)")
# exponent is also possible. the power should be a natural number only.
exp = two ** 3
print(str(two.x) + " ** 3 = " + str(exp.x))
# get a random scalar
rnd_scalar = dumb25519.random_scalar()
print("Random scalar: " + str(rnd_scalar) + " or \n" + str(rnd_scalar.x))

# other Scalar operations in dumb25519:
# comparsion (does not account for overflow), true truncated division ("//"), etc.
# we are done with Scalars.

# differences #2: the elliptic curve points. these are actually points (x,y)
# but the x and y are integers modulo another large (not necessarily prime)
# number q (the value is in dumb25519.q)
# we usually do not initialize points like we initialize scalar. instead, we use
# either one of the two:
# 1) get a random point
rnd_point = dumb25519.random_point()
actual_point = (rnd_point.x, rnd_point.y)   # coords
print("\nRandom point: " + str(rnd_point) + " or \n" + str(actual_point))

# 2) using the "base generator" G
print("Base generator: " + str(dumb25519.G) + " or \n" + str((dumb25519.Gx, dumb25519.Gy)))

# now to produce another point from G (or any other point), we can do, as being said earlier, 
# addition/subtraction of points (G + H, G - H) and scalar multiplication xG for scalar x.
twoG = dumb25519.G + dumb25519.G
zero = dumb25519.G - dumb25519.G
print("G + G = " + str(twoG))
print("G - G = " + str(zero))
# here is the "zero" point:
print("    Z = " + str(dumb25519.Z))
print("Are G - G and Z the same?")
for i in range(15):
    another_point = Scalar(i) * dumb25519.G
    print(str(i) + " * G = " + str(another_point))
print("Those last points look \"random\". This IS a big reason why we use elliptic curves in cryptography:")
print("If I give you a random point P (i.e. from dumb25519.random_point()), it is assumed to be \
impossible to find the x \nsuch that P = xG. The problem of finding x is called \"Discrete Logarithm \
Problem\" (DLP) and the impossibility \nassumption is called Discrete Logarithm (DL) assumption.")

# exercise: what is (-1)G + G ? what is (1/x)*(xG) ? is Z == Z + dumb25519.random_point()?

# cryptographic hash functions
# dumb25519 provides two hash functions: hash_to_scalar() and hash_to_point() that outputs a
# scalar and a point respectively. any data that can be converted to string can be input there.
yet_another_scalar = dumb25519.hash_to_scalar("tutorial", Scalar(12))
yet_another_point =  dumb25519.hash_to_point("tutorial", dumb25519.G)
print("\nHash scalar: " + str(yet_another_scalar))
print("Hash point: " + str(yet_another_point))
# note that the output of hash_to_scalar() is NOT the discrete log of the output of hash_to_point().

# exercise: there is another reason we use elliptic curves: the Diffie-Hellman (DH) key exchange
# implement DH key exchange (just use variables):
#     Alice and Bob wants to share a secret scalar only they would know.
#     Using the generator G and dumb25519.hash_to_scalar(), how would they do it?
# show that after the key exchange, Alice and Bob has a shared secret.

# <your code here>

# if alice_final == bob_final:
    # print("DH key exchange successful.")
# else:
    # print("DH key exchange failed.")

# exercise: Monero cryptocurrency uses Pedersen commitment to hide amounts in the blockchain.
# implement Pedersen commitment: given a scalar x, it must output a pair (r, rG + xH) where r is
# a random scalar. for Monero, r should never be in the blockchain, only the rG + xH is.
#
# then demonstrate the homomorphicity of Pedersen commitment: show that
# pedersen(x1) + pedersen(x2) = (r1 + r2)G + (x1 + x2)H where r1 and r2 are the 'r' output of
# pedersen(x1) and pedersen(x2), respectively.
H = dumb25519.hash_to_point("Pedersen")

def pedersen(amount):
    # <your code here>
    pass

# test for homomorphicity
# commit2 = (r1 + r2) * G + (x1 + x2) * H
# if commit1 == commit2:
    # print("You demonstrated that Pedersen commitment is homomorphic!")
# else:
    # print("Something's wrong :(")

# exercise: implement Elgamal point encryption scheme. this is rarely used 
# because the points are rarely encrypted (if ever).
# here's the scenario:
#     Alice must send the point Y to Bob securely. Bob generates a random keypair (x, xG).
#     x is the private key, and P = xG is the public key to be shared to Alice. Alice encrypts
#     Y using P, and sends the cipher to Bob. Bob then decrypts the cipher using x.
# just like in DH key exchange, just use variables.
# encryption: given a point Y and point P, it must output a pair (rG, Y + rP) where r is a random scalar.
# decryption: given a cipher pair (C1, C2) and a scalar x, output Y = C2 - x * C1.
#
# then demonstrate the homomorphicity of Elgamal encryption scheme. using
# two plaintexts 69000 * H and 420 * H, encrypt both separately, then pairwise add the two ciphers,
# then decrypt the "sum" cipher. what is the decrypted plaintext? 

bob_prvkey = dumb25519.random_scalar()
bob_pubkey = bob_prvkey * dumb25519.G

plain1 = Scalar(69000) * H
plain2 = Scalar(420) * H

def elgamal_enc(plain: Point, bob_pubkey: Point) -> tuple:
    # <your code here>
    pass

def elgamal_dec(cipher: tuple, bob_prvkey: Scalar) -> Point:
    # <your code here>
    pass

# <your code here>

# test for homomorphicity
expected_dec = Scalar(69420) * H
# if actual_dec == expected_dec:
    # print("You demonstrated that Elgamal is homomorphic!")
# else:
    # print("Something's wrong :(")
