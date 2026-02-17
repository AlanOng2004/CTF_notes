# Linearity

A gentle introduction to linear cryptanalysis 🙂

## Recon

```
from random import randint
from hashlib import sha256
from secret import FLAG

V = [randint(0, 100) for i in range(5)]
M = [[V[i] * randint(0, 100) for i in range(5)] for i in range(5)]
C = [M[i // 5 % 5][i % 5] ^ ord(FLAG[i]) for i in range(len(FLAG))]

print(f"{V = }")
print(f"{C = }")
print(sha256(FLAG.encode()).digest().hex())
# V = [14, 38, 56, 76, 51]
# C = [1357, 2854, 1102, 1723, 4416, 283, 344, 4566, 5023, 1798, 477, 3833, 1839, 5416, 4017, 1066, 161, 415, 5637, 1696, 1058, 3025, 5286, 5141, 3818, 1373, 2839, 1102, 1764, 4432, 313, 322, 4545, 5012, 1835, 477, 3825]
# e256693b7b7d07e11f2f83f452f04969ea327261d56406d2d657da1066cefa17
```

We are given lists V and C, and the respective codes for achieving V, M, and C.

Firstly, notice that `C = [M[i // 5 % 5][i % 5] ^ ord(FLAG[i]) for i in range(len(FLAG))]`, which means that every element in C is obtained through an XOR operation with an element in M and a char in FLAG.

Looking at how M is created: 
`M = [[V[i] * randint(0, 100) for i in range(5)] for i in range(5)]`, we see that V[i] is multiplied by a random int (0-100) i times, to create a nested array.

Now we can construct our code to decrypt this algorithmn.

1. We need to figure out the values of M
2. Next, we need to find the corresponding chars of FLAG that will grant us `(V[i] * num) ^ ord(FLAG[i])  = C[i]`
3. We can do this through a bruteforce attack.
4. Lastly, doublecheck the characters we got by encrypting it and comparing with the challenge
    > sha256(cand).hexdigest() == target_hash


## Attempt

```
#!/usr/bin/env python3
# recover_flag_from_VC.py
# Usage: python3 recover_flag_from_VC.py

from collections import defaultdict
from hashlib import sha256
import string

# --- Given data (from your challenge) ---
V = [14, 38, 56, 76, 51]
C = [1357, 2854, 1102, 1723, 4416, 283, 344, 4566, 5023, 1798,
     477, 3833, 1839, 5416, 4017, 1066, 161, 415, 5637, 1696,
     1058, 3025, 5286, 5141, 3818, 1373, 2839, 1102, 1764, 4432,
     313, 322, 4545, 5012, 1835, 477, 3825]
target_hash = "e256693b7b7d07e11f2f83f452f04969ea327261d56406d2d657da1066cefa17"

# --- Alphabet choices: adjust if your flags use a different charset ---
ALPHABET = (string.ascii_lowercase + string.ascii_uppercase +
            string.digits + "{}_-+=, .?!").encode()  # include common punctuation/space
ALPHABET_SET = set(ALPHABET)

n = len(C)

def rc_for_index(i):
    # same mapping as challenge:
    return ((i // 5) % 5, i % 5)

# build mapping from (r,c) -> list of indices i that use M[r,c]
positions = defaultdict(list)
for i in range(n):
    positions[rc_for_index(i)].append(i)

# build candidate M values per (r,c)
candidates = {}
for r in range(5):
    for c in range(5):
        poss = []
        pos_list = positions[(r,c)]
        # choose a base index to propose M from (first one)
        base_i = pos_list[0]
        for p in ALPHABET:               # propose plaintext byte for base position
            M = p ^ C[base_i]            # candidate M that would make base -> p
            # M must be equal to V[c] * k for some k in 0..100
            if V[c] == 0:
                # (not expected in this challenge), require M == 0
                if M != 0:
                    continue
            else:
                if M % V[c] != 0:
                    continue
                k = M // V[c]
                if not (0 <= k <= 100):
                    continue
            # now check that this M produces allowed plaintext bytes for all positions it governs
            ok = True
            plaintext_bytes = {}
            for i in pos_list:
                ch = M ^ C[i]
                if ch not in ALPHABET_SET:
                    ok = False
                    break
                plaintext_bytes[i] = ch
            if not ok:
                continue
            # store candidate: (M, plaintext_bytes dict)
            poss.append((M, plaintext_bytes))
        candidates[(r,c)] = poss

# diagnostics
prod = 1
for key in sorted(candidates.keys()):
    cnt = len(candidates[key])
    print(f"{key}: {cnt} candidate(s)")
    prod *= max(1, cnt)
print("Upper-bound product of choices:", prod)

# If any cell has zero candidates, you may need to widen ALPHABET
zeros = [k for k,v in candidates.items() if len(v)==0]
if zeros:
    print("Warning: some cells have 0 candidates:", zeros)
    print("Try widening ALPHABET (include more punctuation or whitespace).")
    # Don't exit yet — sometimes a larger alphabet is needed.

# order by fewest candidates first
items = sorted(candidates.items(), key=lambda kv: len(kv[1]))
keys = [it[0] for it in items]
vals = [it[1] for it in items]

# helper to assemble full flag bytes from assignment map
def build_flag_bytes(assign):
    out = bytearray(n)
    for i in range(n):
        r,c = rc_for_index(i)
        M = assign[(r,c)]
        out[i] = M ^ C[i]
    return bytes(out)

# optional prefix pruning (uncomment to enforce a known prefix)
# prefix = b"infobahn{"
prefix = None

found = []
def backtrack(idx, assign):
    if idx == len(keys):
        cand = build_flag_bytes(assign)
        if sha256(cand).hexdigest() == target_hash:
            try:
                print("FOUND FLAG:", cand.decode())
            except:
                print("FOUND FLAG (raw):", cand)
            found.append(cand)
            return True
        return False
    k = keys[idx]
    for (M, pbytes) in vals[idx]:
        # quick prefix prune
        if prefix is not None:
            ok = True
            for pos, ch in pbytes.items():
                if pos < len(prefix) and ch != prefix[pos]:
                    ok = False
                    break
            if not ok:
                continue
        assign[k] = M
        if backtrack(idx+1, assign):
            return True
        del assign[k]
    return False

print("Starting search...")
if backtrack(0, {}):
    print("Done.")
else:
    print("No solution found with current alphabet/constraints.")
    if not zeros:
        print("Consider enabling prefix pruning or widening ALPHABET.")
```

Running this code decrypts the given values and gives us the flag!

FOUND FLAG: infobahn{You_HAVE_Aff1niTy_f0rCrypto}