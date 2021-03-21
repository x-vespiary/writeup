# LINE CTF 2021 - Crypto - babycrypto3

```txt
$ ./msieve -q -v -t 16 -e

Msieve v. 1.53 (SVN unknown)
Sat Mar 20 10:16:39 2021
random seeds: 341f86e1 eead51a2
factoring 31864103015143373750025799158312253992115354944560440908105912458749205531455987590931871433911971516176954193675507337 (119 digits)
searching for 15-digit factors
searching for 20-digit factors
searching for 25-digit factors
200 of 214 curves
completed 214 ECM curves
searching for 30-digit factors
ECM stage 2 factor found
p42 factor: 291664785919250248097148750343149685985101
p78 factor: 109249057662947381148470526527596255527988598887891132224092529799478353198637
elapsed time 00:01:27
```

```py
from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes, bytes_to_long

f = open('pub.pem', 'r')
key = RSA.importKey(f.read())

p = 291664785919250248097148750343149685985101
q = 109249057662947381148470526527596255527988598887891132224092529799478353198637

with open('ciphertext.txt', 'rb') as f:
    c = bytes_to_long(f.read())
    d = pow(key.e, -1, (p-1)*(q-1))
    m = pow(c, d, key.n)
    print(long_to_bytes(m))
```

```sh
❯ python a.py
b'\x02`g\xff\x85\x1e\xcd\xcba\xe5\x0b\x83\xa5\x15\xe3\x00Q0xPU0lORyBUSEUgRElTVEFOQ0UuCg==\n'

❯ echo -n Q0xPU0lORyBUSEUgRElTVEFOQ0UuCg== | base64 -d
CLOSING THE DISTANCE.
```

`LINECTF{CLOSING THE DISTANCE.}`