def rol3(x):
    return ((x << 3) | (x >> 5)) & 0xff

expect_0 = [
        0x66, 0x86, 0x6, 0x6
]

print("".join(chr(rol3(b)) for b in expect_0))
