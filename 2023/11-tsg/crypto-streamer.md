# Streamer

[video](https://www.youtube.com/live/9IUsP3CBwZc?si=nZ_dmdkSEilRAF7_&t=1128)


As a first "TSGCTF{" and "==} " to recover a portion of the key.
I restored the key one character at a time so that the flags are natural While being aware of the flag patterns and Base64 character types.
When there were only 3 bytes left, I used brute force to identify the flag.

```py
import secrets
import hashlib
import base64
import re
import string
import sys

pattern = re.compile("[a-zA-Z0-9!-/:-?\[-`|~]+")

def check(flag):
    return pattern.fullmatch(flag[7:-26])

key_stream = [247, 176, 17, 0, 156, 72, 203, 232, 13, 179, -1, -1, -1, 41, 241, 70]
cipher = [163, 227, 86, 67, 200, 14, 176, 188, 101, 214, 117, 82, 99, 71, 199, 117, 139, 130, 78, 43, 224, 101, 183, 219, 82, 213, 70, 95, 101, 118, 133, 46, 146, 239, 98, 97, 250, 123, 183, 218, 82, 218, 1, 97, 62, 29, 145, 105, 168, 136, 116, 95, 253, 59, 148, 132, 98, 207, 118, 66, 52, 118, 197, 98, 168, 201, 126, 117, 195, 61, 184, 141, 82, 210, 86, 98, 47, 118, 144, 58, 221, 192, 99, 48, 224, 98, 185, 129, 108, 152, 25, 97, 96, 85, 173, 58, 148, 194, 104, 124, 182, 99, 162, 216, 99, 157, 117, 106, 59, 64, 213, 25, 148, 217, 109, 42, 224, 101, 183, 219, 127, 236, 67, 26, 12, 29, 174, 118, 153, 213, 78, 43, 245, 52, 151, 199, 113, 214, 117, 66, 121, 72, 141, 111, 168, 194, 112, 43, 244, 123, 183, 218, 82, 199, 86, 19, 47, 29, 141, 26, 139, 239, 112, 95, 239, 99, 185, 141, 57, 222, 117, 22, 58, 89, 153, 117, 133, 156, 78, 98, 233, 60, 148, 129, 121, 236, 67, 26, 12, 64, 159, 53, 196, 152, 100, 124, 174, 45, 148, 138, 104, 155, 75, 75, 32, 76, 174, 47, 131, 239, 100, 115, 175, 59, 148, 156, 101, 214, 117, 26, 103, 85, 173, 105, 139, 213, 78, 114, 168, 38, 175, 135, 96, 236, 68, 75, 62, 17, 194, 52, 211, 239, 99, 101, 224, 98, 248, 220, 38, 128, 86, 23, 63, 80, 223, 25, 146, 222, 123, 111, 229, 23, 163, 137, 101, 210, 66, 95, 12, 19, 220, 111, 218, 138, 56, 45, 166, 97, 139, 188, 90, 195, 28, 77, 2, 113, 152, 34, 165, 252, 88, 67, 250, 44, 163, 167, 64, 234, 1, 119, 18, 20, 204, 59]

# print(cipher[-3] ^ ord("="))

target = 10
for t in range(256):
    print(t, file=sys.stderr)
    for k in range(256):
        for j in range(256):
            key_stream[target] = j
            key_stream[target+1] = k
            key_stream[target+2] = t

            encrypted_flags = []
            flag = []
            isOk = True

            for i in range(len(cipher)):
                index = i%16
                if index < len(key_stream):
                    if key_stream[i%16] != -1:
                        value = cipher[i]^key_stream[i%16]
                    else:
                        value = ord("0")
                    if value not in string.printable.encode():
                        isOk = False
                        break
                    flag.append(chr(value))
                else:
                    flag.append("0")
            flag = "".join(flag)
            if isOk and check(flag):
                flag_content = flag[7:-26].encode()
                flag_hash = hashlib.md5(flag_content).digest()
                hoge = b"TSGCTF{"+flag_content+b"@"+base64.b64encode(flag_hash)+b"}"
                if hoge.decode() == flag:
                    print(hoge)
```