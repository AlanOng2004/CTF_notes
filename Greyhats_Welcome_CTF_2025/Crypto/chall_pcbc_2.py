import os
import binascii

new_iv = bytes.fromhex("00000000000000000000000000000000")



iv = bytes.fromhex("e0a0ca86dbb246a1ad7dd60eb85f22b2")
pt = bytes.fromhex("3f15a2a6f6ebf4dd6385b89bccdea725012da03acfca2ea698778775f7360da00a903c997170eb66906925d1661bc7f30b1d474ab9d40a839b05ee65fda147691a85b09d88423801fd2e7887ea1fa6cac8755ce63b4b792229788e6be1085e9b2fa88c4d89f87903cf4eb28c16ba51568d3de9daca15131fe65bfa11fe4fe202aad31cfae29c245618669bef2e7395bf15b92b25f3105a9e8b0336494cc61a2b")

chunks = [pt[16*i:16*i+16] for i in range(len(pt)//16)]

def xor(a, b, c):
    return bytes(x ^ y ^ z for x, y, z in zip(a, b, c))
for i in range(len(chunks)):
    pt0_prime = xor(new_iv, chunks[i], iv)
    print(pt0_prime.hex())
    
print("line break")
print(new_iv.hex())
