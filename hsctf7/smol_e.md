# Smol E

### 問題概要
平文m1,m2をRSA暗号化した暗号文c1,c2が与えられる。
m1とm2の上位bitは共通している。
e = 3, n が与えられる。
平文を求めよ。

### Writeup
下の記事の Coppersmith’s Short Pad Attack & Franklin-Reiter Related Message Atotack を参照。
[SageMathを使ってCoppersmith's Attackをやってみる - ももいろテクノロジー](http://inaz2.hatenablog.com/entry/2016/01/20/022936)

ここに載っていることをすると、m1,m2が求めれる。

padding が何bitか不明なので、全探索する。

```py
m = 1426051161596273413795556654328320105145439332147585418507576775870780450590379567453641429082640842935901398525237698534587016076610446383728128936582478631369081375319103785503713430762835018940932512662482247881629813321166872870577809910090459052486979919351413039719867069160

for i in range(8):
    s = hex(m)[2:]
    if len(s) % 2 != 0:
        s = '0' + s
    s = bytes.fromhex(s)
    print(s)
    m //= 2

```

`b"Press Point F to pay respects. I'm writing this a day before HSCTF starts. flag{n0t_4_v3ry_sm0l_fl4g}\n\x00\x00\x00\x00\x00\x00\x00\x00\xfcKU$\xd9t"`

という出力が得られる。

`flag{n0t_4_v3ry_sm0l_fl4g}`