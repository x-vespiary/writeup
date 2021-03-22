# LINE CTF 2021 - Crypto - babycrypto4

Unknown bits of `k` is small, so I searched valid `k` by brute force.

Each signature used same signing key(`d`). If true `k` is recoverd, we can calculate `d` by `d = (ks - z) / r`.

I calculated candidates of `d` from a signature. Next, I calculated another candidates of `d` from the other signature. Finally, the intersection of the two candidates is `d`.

## Code

```python
from Crypto.Util.number import long_to_bytes


if __name__ == "__main__":
    with open("./output.txt") as f:
        raw = f.readlines()

    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF7FFFFFFF
    a = -3
    b = 0x1C97BEFC54BD7A8B65ACF89F81D4D4ADC565FA45
    order = 0x100000000000000000001f4c8f927aed3ca752257

    g_x = 0x4A96B5688EF573284664698968C38BB913CBFC82
    g_y = 0x23A628553168947D59DCC912042351377AC5FB32

    curve = EllipticCurve(a, b, p)
    G = ECPoint(g_x, g_y, curve)

    rs = []
    ss = []
    ks = []
    zs = []
    for line in raw:
        params = line.strip().split(" ")
        rs.append(int(params[0], 16))
        ss.append(int(params[1], 16))
        ks.append(int(params[2], 16))
        zs.append(int(params[3], 16))

    d_candidates = set()
    for i in range(0x10000):
        k = ks[0] + i
        r = rs[0]
        s = ss[0]
        z = zs[0]

        d = (s*k - z) * pow(r, -1, order) % order
        d_candidates.add(d)

    print(len(d_candidates))

    for i in range(0x10000):
        k = ks[1] + i
        r = rs[1]
        s = ss[1]
        z = zs[1]

        d = (s*k - z) * pow(r, -1, order) % order
        
        if d in d_candidates:
            print("[+] Found!!")
            print(hex(d))
            break
```

## Flag

`LINECTF{0c02d451ad3c1ac6b612a759a92b770dd3bca36e}`

I could find `d`, but the flag format(`LINECTF{<encryption key>}`) confused us. In addition, I didn't notice leading 0 was needed. Thanks to my teammate, he noticed that and we got the flag, but wasted a lot of time.
