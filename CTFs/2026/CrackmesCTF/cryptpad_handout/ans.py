data = bytes.fromhex(
"c9988fc7a61c026be206f35249162759455c4c47bc4e28a62f71c7d806854203"
"08507d93f5fee599484e822be200572616f6b41c000000e8171bf4503f3d7008"
)

# Test: XOR with index
decoded = bytes(data[i] ^ i for i in range(len(data)))
print(decoded)

# Test: XOR with (index % 256)
decoded = bytes(data[i] ^ (i & 0xff) for i in range(len(data)))
print(decoded)

# Test: XOR with (i * 7)
decoded = bytes(data[i] ^ ((i * 7) & 0xff) for i in range(len(data)))
print(decoded)

