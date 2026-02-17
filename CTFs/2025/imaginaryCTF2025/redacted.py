cipher_hex = "65 6c ce 6b c1 75 61 7e 53 66 c9 52 d8 6c 6a 53 6e 6e de 52 df 63 6d 7e 75 7f ce 64 d5 63 73"
cipher_bytes = bytes.fromhex(cipher_hex)

# We know flags start with "ictf{"
known_plain = b"ictf{"

# Derive key from first few bytes
key = bytes([c ^ p for c, p in zip(cipher_bytes, known_plain)])
print("Recovered key fragment:", key)

# Try applying repeating key
full_plain = bytes([c ^ key[i % len(key)] for i, c in enumerate(cipher_bytes)])
print(full_plain.decode(errors="ignore"))
