# Androids Encryption [Crypto]

written by Xornet

- Score: 115
- Solves: 108

## 問題概要

### PCBCモードについて

- 参考 -> <https://ja.wikipedia.org/wiki/%E6%9A%97%E5%8F%B7%E5%88%A9%E7%94%A8%E3%83%A2%E3%83%BC%E3%83%89#Propagating_Cipher_Block_Chaining_(PCBC)>

CBCモードと違うのは暗号化時に次の平文ブロックとXORを取るのが暗号文ブロックだけでなく平文ブロックともXORをとっている。

具体的には次のような関係がある

```python
"""
    c: 暗号文ブロック
    p: 平文ブロック
    iv: 初期ベクトル, 次の暗号化前に平文にXORさせる要素
"""
c[i] = encrypt(p[i] ^ iv[i])
iv[i] = p[i-1] ^ c[i-1] if i > 0 else iv[0]
```

よってこれに対する復号手順は次のようになる

```python
p[i] = decrypt(c[i]) ^ iv[i]
iv[i] = p[i-1] ^ c[i-1]
```

ただし`^`演算子は同じ長さの2つのバイト列を各文字毎に排他的論理和をとったものである。

問題中では暗号化手順のみ与えられて復号手順は与えられないのでまずそれを書く必要がある。実際に書いたのは次の通り(`to_blocks, xor`はサーバー側で使われている関数)

```python
def decrypt(cipher_text, key, iv):
    cipher_blocks = to_blocks(cipher_text)
    plain_blocks = []
    aes = AES.new(key, AES.MODE_ECB)

    for block in cipher_blocks:
        xored = aes.decrypt(block)
        plain = xor(xored, iv)
        plain_blocks.append(plain)
        iv = xor(plain, block)

    return b"".join(plain_blocks)
```

### サーバーの仕様

コードは[こちら](server.py)

実際の問題中では次の3つから行う動作を1つ選ぶ事ができる

1. base64エンコードで送られてきた平文をデコードして平文ブロック(サイズは128bit)に分割して暗号化し、その結果を送り返す

2. フラグを暗号化しその結果をくれる、但し鍵とIVは1. の暗号化手順で用いたものとは異なる上にこれは毎回変わってしまう。

3. 終わり

これらは3を選択するまで何回も繰り返すことが出来る。

以下では鍵とIVに関して混同しないように1の暗号化で使う鍵, IVをそれぞれ鍵1, IV1とおき、2の暗号化でつかうそれらを鍵2, IV2とおく。

鍵2, IV2はいずれの暗号化手順を実行すると変わってしまうが、次のような関係があるので鍵2に関しては次のブロックのものを特定できる

- 鍵2: 前回の暗号化ブロック全てで排他的論理和を取ったもの
- IV2: 前回のIV2を鍵2で復号したもの(`decrypt(key2, iv2)`)

いずれの暗号化の場合も返される暗号文は先頭にIV(128bit)が付いており、残りが暗号文ブロックの結合である。したがって返される暗号文から次回使われる鍵2と今回使われたIV(1, 2を問わない)は判明する。

ということで次のような手順を経ることで2の暗号化で得た暗号文からフラグを復号することが出来る。

1. 何らかの平文を用意して1の暗号化を行う

2. 返された暗号文からIV以外の部分を取り出し、ブロック毎に分割してXORをとることで次の鍵2を得る

3. 2の暗号化を行って暗号文を入手し、先頭128bitからIV2を得る

4. 暗号文, 鍵2, IV2が手に入ったので自前の復号手順で復号する

## Exploit Code

[here](exploit.py)

## Flag

`CTF-BR{kn3W_7h4T_7hEr3_4r3_Pc8C_r3pe471ti0ns?!?}`

## 感想

本CTFの癒やし問題
