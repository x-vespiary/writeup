# LINE CTF 2021 - Crypto - babycrypto2

```py
#!/usr/bin/env python
from base64 import b64decode, b64encode

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


class AESCipher:
    def __init__(self, key):
        self.key = key

    def encrypt(self, data):
        iv = get_random_bytes(AES.block_size)
        self.cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return b64encode(iv + self.cipher.encrypt(pad(data,
                                                      AES.block_size)))

    def encrypt_iv(self, data, iv):
        self.cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return b64encode(iv + self.cipher.encrypt(pad(data,
                                                      AES.block_size)))

    def decrypt(self, data):
        raw = b64decode(data)
        self.cipher = AES.new(self.key, AES.MODE_CBC, raw[:AES.block_size])
        return unpad(self.cipher.decrypt(raw[AES.block_size:]), AES.block_size)


token = b"ZzTosTPcUnBu44roqYGeyIjyJ22OoYp66c67bitZZthoRjCwTC9sW5jOFkVqW7WlMwJqI5Y+eJtxCkY4lkVkX3vzdDSkPtwB1FOrfHWPeGq4jOeprbrqhtcQzRdUsukyF1YdRzzZ8ezm2g82ydjFYcDrkfzk3ZQOzx0CpVulL80HGbwsB6amUMsmmVsC4jULWpg66++vj30B6p/aKGbh"
test_command = "X05PCR4VfeCWgbO4WOg0P9FRaRRgaPdE4PTrm370iRtTxrC5ty3cfApwL7FCuk5vszs+5J6mbyxtKZj8Ys5MkTfP1P4oqdHIlz8q9LDnotMejlveXz9AOvzuZuR5BmW0dbhVMxX6vtEKEMEGqBWC/tJOFRjFaEjfoxnN5edF0GMiRSnhdHDG6qqc6Lps/EV8kvbK20iNn0mPTkF5RoJj9/72fRINw+LeObfXWdatf1cjKGV0AibIudk5IocSXVIGlb2Dgtml16Bn0f7ywOAbJMM8AHm7fy8VLrXNZXjH2gQuZg679reNATUK77aBln8RGNaMxhm+fHMtqy2+FOqWmA=="
show_command_raw = (b"Command: show" + token)[:AES.block_size]
test_command_raw = (b"Command: test" + token)[:AES.block_size]

test_command_body = b64decode(test_command)[AES.block_size:]
test_command_body_first_block = test_command_body[:AES.block_size]
iv = b64decode(test_command)[:AES.block_size]

print(iv)
print(test_command_body_first_block)
print(show_command_raw)

iv_send = bytes([iv[i] ^ test_command_raw[i] ^ show_command_raw[i]
                 for i in range(len(iv))])
print(iv_send)

show_command = b64encode(iv_send + test_command_body)
print(show_command)
```

`LINECTF{echidna_kawaii_and_crypto_is_difficult}`