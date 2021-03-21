# LINE CTF 2021 - Crypto - babycrypto1

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


test_command = "kbuuTp1iSuv4soT/RS7MNe6VNfi93SaBcPy1LhupUhgoDL8WJ4bM2Yqbq7vag37fB8igMHistB1zZJObM9XtCyCCX+zUbfzJyUNU0bW3p7iWFY/ySQwEQ7rbaoJxKzNCd+EwU6O1TzVNQ6QFnd0n2Anb/Dc0N9wjX6fDlNftw3KCttGZ6M7HBbaYqK1qLg8iwgvA3/C/VIAt1gxdcfhKvjHe+nv5vdpt/OXl3L+wDs+J4zA6roZ+aoyCi247NJNl" # Edit
iv = b64decode(test_command)[AES.block_size*-2:AES.block_size*-1]
print(b64encode(iv))
msg = b"show"
print(b64encode(msg))
ciphertext = "Md76e/m92m385eXcv7AOz6fTZTJLKcgGsl47/xl6tg4="
show_command = b64decode(test_command)[
    :AES.block_size*-1] + b64decode(ciphertext)[AES.block_size:]
show_command = b64encode(show_command)
print(show_command)
```

`LINECTF{warming_up_crypto_YEAH}`
