#!/usr/bin/env python3

import os, sys

# collect args
if len(sys.argv) == 3:
    in_file = sys.argv[2]
    out_file = sys.argv[1]
else:
    in_file = "first_password.pdf"
    out_file = "bathhouse_password"


with open(in_file, "rb") as f:
    contents = f.read()

key = b"\xf3\x8f\x03\x69"
out = b""
for i in range(len(contents)):
    out += bytes([contents[i] ^ key[i % len(key)]])

with open(out_file, "wb") as f:
    f.write(out)
