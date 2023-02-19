# elliptic curve cryptography tutorial/playground (part 4)

import dumb25519

# this is about the so called "cofactor" of elliptic curves.
# the secp256k1 curve, used in Bitcoin, has cofactor = 1.
# while ed25519 curve, used in Monero, has cofactor = 8. What does this mean?
# the cofactor > 1 means that the "whole" group of points in elliptic curve
# contains points that we do not (and SHOULD NOT) use. More precisely,
#
# cofactor = (total number of points of elliptic curve group) / (number of USABLE points)
#
# where in the number of USABLE points should be a HUGE PRIME number,
# and for ed25519, this is the value of dumb25519.l in dumb25519.py.
# note 1: if you're familiar in basic group theory, the usable points form a "subgroup" of the whole group.
# note 2: in dumb25519.py code, this group of usable points is called the "main subgroup".
#
# now you can have questions:
#
# 1) why not just use the whole group? isn't that stronger because the whole group has more points
# than just the usable points, and larger number = stronger, right?
#
#     there's an easy way (for computers) to reduce the discrete log problem of the whole group
#     to the discrete log of its largest subgroup, which goes back to the usable points.
#     so either way, we have to rely on the difficulty of the discrete log of usable points.
#     see [1] for the description of reduction.
#
# 2) why not just use secp256k1 then, if its cofactor = 1 looks simpler?
#
#     I cannot say which is "better". I think both curves are fine.
#
#     however, unlike the zero point of ed25519 (this is the dumb25519.Z in dumb25519.py),
#     the zero point of secp256k1 doesn't really exist as a point (x,y)!
#     this zero "point" is the so called "point at infinity", in which you somewhat force its
#     zeroness (i.e. X + Z = Z + X = X) in curve implementations (in affine coordinates).
#     this is among the "many edge cases and subtle death traps"[1] of math of elliptic curves.
#
#     as for Monero choosing ed25519, I don't know really. this goes back to the CryptoNote whitepaper.
#
# 3) are there potential implementation vulnerabilities from curves with cofactor > 1?
#
#     yes. see the "key image bug" section below.
# 
# phew! this concludes the series. no more next parts in the future.
# let's see if I manage to upload a new prototype, I cannot promise anything. See ya!
#
# reference:
# [1] https://loup-vaillant.fr/tutorials/cofactor. note that this is a dense technical article
# about cofactor and group theory.

# The following is a demonstration of "Key Image Bug" discovered in Monero in 2017.
# This demonstrates a pitfall of having an elliptic curve with cofactor > 1.
# Source: https://www.getmonero.org/2017/05/17/disclosure-of-a-major-bug-in-cryptonote-based-currencies.html

# Generator for the small subgroup of size of the cofactor = 8
# Source: https://monero.stackexchange.com/a/8672
G_small = dumb25519.Point('c7176a703d4dd84fba3c0b760d10670f2a2053fa2c39ccc64ec7fd7792ac03fa')

# Aim: double spend!

# Let's say you are an attacker, and you have your key image.
# Key images are in main subgroup, as random_point always outputs.
key_image = dumb25519.random_point()

# For your attack to be possible, make sure that somewhere in tx verification,
# your key image will be multiplied to a Scalar that is a multiple of cofactor = 8.
# Since you initiate the tx, you can always check, but you cannot always choose
# the Scalar. Instead, you try producing proofs again and again until getting the
# desired Scalar. Thanks to "non-interactive" proof, producing proofs do not
# require verifier interaction ;)
tx_ver_scalar = dumb25519.Scalar(1)
while tx_ver_scalar % 8 != dumb25519.Scalar(0):
    tx_ver_scalar = dumb25519.random_scalar()

# Ok you check that the attack is possible. Let's now create 7 more fake key images!
ki_list = []

for i in range(dumb25519.cofactor):
    ki_new = dumb25519.Scalar(i) * G_small + key_image
    print(f'Key image #{ i }: { ki_new }')   # Key image #0 is your original key_image
    ki_list.append(ki_new)

# Are they unique to each other?
ki_set = set([str(i) for i in ki_list])
print(f'Distinct key images: { len(ki_set) }\n')

# So you initiated 8 tx's. Same coins, different "key images".
# Now the verifiers check the tx's. Somewhere there, tx_ver_scalar is being multiplied
# to your 8 "key images"
prod_list = [i * tx_ver_scalar for i in ki_list]

# Let's take a look
print('After multiplying a Scalar that is a multiple of cofactor = 8 to the key images')
print('to simulate tx verification...')
for i, j in enumerate(prod_list):
    print(f'Product point #{ i }: { j }')

# Are they unique to each other?
prod_set = set([str(i) for i in prod_list])
print(f'Distinct product points: { len(prod_set) }\n')

if len(prod_set) == 1:
    print('Theoretical double spend (actually "8 times" spend) committed successfully!!!')

# How to mitigate this?
# The most elegant and general solution is to use Ristretto (https://ristretto.group/).
# For Monero, there is a simpler solution. To quote from the getmonero.org source above:
#
#     To mitigate, check key images for correctness by multiplying by the curve order l.
#     Check that the result is the identity element.
#
# Let's do this for ki_list.
#
# Note: use dumb25519.Scalar('l') for (main subgroup) order 'l'. I know I know, 'l' is technically
# NOT a Scalar, but that's where the first four letters of "dumb25519" come in :D

# check_condition = lambda point: <your code here>   # check_condition : point -> boolean

# print('\nAfter multiplying the curve order l to the key images...')
# for i, j in enumerate(ki_list):
    # print(f'Product point #{ i }: { j } => { check_condition(j) }')

# print('Only the #0, corresponding to the original key_image, is the TRUE key image!')

# See https://github.com/monero-project/monero/pull/1744/commits/d282cfcc46d39dc49e97f9ec5cedf7425e74d71f#diff-1fb58b51f281d178c1a564bccf94bc813261a1fd585a9372e3d53999a25f9a53R714
# for the actual mitigation in Monero
