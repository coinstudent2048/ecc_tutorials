# elliptic curve cryptography tutorial/playground (part 2)

from dumb25519 import Scalar, ScalarVector, Point, PointVector
import dumb25519

# this is about vectors of scalars (ScalarVector) and of points (PointVector).
# we can think of a vector as an array of data.

# ScalarVector initialize
print("-------------------------- ScalarVector --------------------------")
pre_x1 = [Scalar(1), Scalar(2), Scalar(3)]
x1 = ScalarVector(pre_x1)
pre_x2 = [Scalar(4), Scalar(5), Scalar(6)]
x2 = ScalarVector(pre_x2)

# element-wise operations
print("Addition:", x1 + x2)
print("\nSum of all:", x1.sum())
print("\nSubtraction:", x1 - x2)
print("\nNegation:", -x1)
print("\nMultiplication:" , x1 * x2)
print("\nDivision:", x1 * x2.invert())

# array operations
print("\nSlice:", x1[:2])
print("\nLength:", len(x1))
x3 = x1[:]
x3.extend(x2)
print("\nExtend:", x3)

# dot product: sum([x1[i] * x2[i] for i in range(len(x1))])
print("\nDot product:", x1 ** x2)

# note: the "standard" str output of Scalar and Point is in Hex.
# please read dumb25519.py code for better understanding of ScalarVector.

# PointVector initialize
print("\n-------------------------- PointVector --------------------------")
pre_y1 = [dumb25519.G * Scalar(1), dumb25519.G * Scalar(2), dumb25519.G * Scalar(3)]
y1 = PointVector(pre_y1)
pre_y2 = [dumb25519.G * Scalar(4), dumb25519.G * Scalar(5), dumb25519.G * Scalar(6)]
y2 = PointVector(pre_y2)

# element-wise operations
print("Addition:", y1 + y2)
print("\nSubtraction:", y1 - y2)
print("\nScalar Multiplication:", Scalar(2) * y1)

# array operations
print("\nSlice:", y1[:2])
print("\nLength:", len(y1))
y3 = y1[:]
y3.extend(y2)
print("\nExtend:", y3)

# multiscalar multiplication: sum([x1[i] * y2[i] for i in range(len(x1))])
# this is like the dot product above, except that this is multiplication
# between ScalarVector and PointVector.
print("\nExpected Multiscalar Mult:", (x1 ** x2) * dumb25519.G)
print("  Actual Multiscalar Mult:", x1 ** y2)
print("The two are equal right?")

# please read dumb25519.py code for better understanding of PointVector.

# exercise: implement Shamir secret sharing
# read more: https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing
# here's the scenario:
#     You know a secret. you call n other people (which we call 'players').
#     You must give each player a "partial key" so that exactly m people (with m <= n)
#     is required to recover the secret. how would you do that?
# Shamir secret sharing allows you to do this!

# here's the actual secret. the players must not know this (until recovery at least)
actual_secret = Scalar(123456789)

# build the secret polynomial: we want m = 3 players to recover the secret
# hence len(poly) should be 3, or in other words, degree of polynomial should be 2.
# set coeff[0] = actual_secret, and the other coeff must be random scalars.
# note: coeff[0] corresponds to x ** 0 = 1, coeff[1] corresponds to x ** 1 = x,
#       coeff[2] corresponds to x ** 2, etc.
# pre_poly = [None for i in range(3)]
# <your code here>
# poly = ScalarVector(pre_poly)

# polynomial evaluation poly(x)
#    * coeff: ScalarVector of coefficients
# note: coeff[0] corresponds to x ** 0 = 1, coeff[1] corresponds to x ** 1 = x,
#       coeff[2] corresponds to x ** 2, etc.
def poly_eval(x: Scalar, coeff: ScalarVector) -> Scalar:
    powers_x = ScalarVector()
    powers_x.append(Scalar(1))
    for i in range(len(coeff) - 1):
        powers_x.append(x * powers_x[i])
    return powers_x ** coeff

# list of n = 5 'players'/x-coord of share coords
# note: Scalar(0) is not allowed in player_list because poly(0) = secret (which leaks the secret)
player_list = [Scalar(1), Scalar(2), Scalar(3), Scalar(4), Scalar(5)]

# build all share coords. these are the "partial keys" to be sent to the players
# all_coords = []
# for xi in player_list:
    # all_coords.append((xi, poly_eval(xi, poly)))

# recover the secret: implement the formula in the following link:
# https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing#Computationally_efficient_approach
#    * coords: set of coords for recovery
# note: our "division" is (x1 * x2.invert()), NOT (x1 // x2) !!!
def recover(coords: list) -> Scalar:
    # <your code here>
    pass

# here's a 3 coords to recover secret:
# experiment: what would happen if 1) you change some indexes?, and 2) add/remove coords?
# recover_coords = [all_coords[0], all_coords[2], all_coords[4]]

# recovered_secret = recover(recover_coords)
# if recovered_secret == actual_secret:
    # print("\nThe implementation of Shamir secret sharing works!")
# else:
    # print("\nThere's a problem in implementation of Shamir secret sharing.")
