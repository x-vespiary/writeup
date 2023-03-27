# LINE CTF 2023 - Crypto - Malcheeeeese

```python
import json
from base64 import b64encode, b64decode

from pwn import remote, xor


b64_pwd = b"Y2hlZWVlZXNl===="  # cheeeeese
b64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

io = remote("34.85.9.81", int(13000))


def oracle(payload):
    assert len(payload) == 136
    io.sendline(payload.hex().encode())
    ret = io.recvline().strip().decode()
    try:
        ret = json.loads(ret)
    except:
        print(ret)
    return ret


_ = io.recvuntil(b"Leaked Token:")
ct = bytes.fromhex(io.recvline().strip().decode())
enc_pwd = ct[12: 12+16]


# reuse iv
iv = b64decode(ct[:12])
new_iv = iv + b"\x00"


# recover prev pwd
b64_prev_pwd = ""
for _ in range(16):
    size = len(b64_prev_pwd)
    if size in [0, 1]:
        cands = []
        for c in b64_chars:
            tmp_enc_pwd = enc_pwd[:15 - size] + xor((c + b64_prev_pwd).encode(), b"=" * (1 + size), enc_pwd[15 - size:16])
            payload = b64encode(new_iv) + tmp_enc_pwd + ct[12 + 16:]
            ret = oracle(payload)
            print(c, ret)
            if ret["pwd_len"] == 12 - 1 - size // 4 * 3 - [0, 1, None, 2][size % 4]:
                cands.append(c)
        if len(cands) == 1:
            c = cands[0]
            b64_prev_pwd = c + b64_prev_pwd
            print(b64_prev_pwd)
        else:
            raise ValueError
    elif size % 4 in [0, 1]:
        assert size >= 4
        cands = []
        for c in b64_chars:
            tmp_enc_pwd = enc_pwd[:15 - size] + xor((c + b64_prev_pwd).encode(), b"=" * (size % 4 + 4 - 3) + b"A===" + b"====" * (size // 4 - 1), enc_pwd[15 - size:16])
            payload = b64encode(new_iv) + tmp_enc_pwd + ct[12 + 16:]
            ret = oracle(payload)
            print(c, ret)
            if ret["pwd_len"] == 12 - 1 - size // 4 * 3 - [0, 1, None, 2][size % 4]:
                cands.append(c)
        if len(cands) == 1:
            c = cands[0]
            b64_prev_pwd = c + b64_prev_pwd
            print(b64_prev_pwd)
        else:
            raise ValueError
    else:
        pwd_lens = []
        for c in b64_chars:
            tmp_enc_pwd = enc_pwd[:15 - size] + xor((c + b64_prev_pwd).encode(), b"=" * (1 + size), enc_pwd[15 - size:16])
            payload = b64encode(new_iv) + tmp_enc_pwd + ct[12 + 16:]
            ret = oracle(payload)
            print(c, ret)
            pwd_lens.append(ret["pwd_len"])
        cands = []
        for c in b64_chars:
            valid_b64 = []
            for d in b64_chars:
                try:
                    _ = b64decode(b"A" * (3 - size % 4) + xor(c.encode(), d.encode(), b"=") + b"=" * (size % 4) + b"=" * 4)
                    valid_b64.append(True)
                except:
                    valid_b64.append(False)
            if valid_b64 == list(map(lambda x: x != -1, pwd_lens)):
                cands.append(c)
        if len(cands) == 1:
            c = cands[0]
            b64_prev_pwd = c + b64_prev_pwd
            print(b64_prev_pwd)
        else:
            raise ValueError

# b64_prev_pwd = "xRlZzM+2n6KP7xoV"
prev_pwd = b64decode(b64_prev_pwd)

cur_enc_pwd = xor(enc_pwd, b64_prev_pwd.encode(), b64_pwd)
payload = b64encode(new_iv) + cur_enc_pwd + ct[28: -3] + xor(ct[-3: -2], b"A", b"B") + ct[-2:]
ret = oracle(payload)
print(ret["flag"])
```

`LINECTF{c576ff588b07a5770a5f7fab5a92a0c2}`
