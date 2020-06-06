# Evil Stego

## Writeup

At first, I try extracting informations from [out.png](out.png) by LSB Steganography (I used the tool "Aoisora wo miagereba soko ni siroi neko" made by Japanese). The results shows [github link](https://github.com/evil-steganography/evil-stego-1) to steganography code are embed to top red pixel.

![link_to_github](img/attach1.PNG)

In this repo, there is steganography [code](main.py) that mey be used by this challenge.

### Steganography

I found some features in this stego.

1. At first, 32bit seed is generated. And `random.seed(bytes(seed))` is executed.
2. The bytes: `b"\x90\xbfhttps://github.com/evil-steganography/evil-stego-1" + bytes(seed) + pack("<I", size)` are embed to top red pixels.  
`size` is the length of message.
3. Embed pixels are selected by `locations = random.sample(valid_spots[c:], size * 8 + 1)`.  
`valid_spots` is the list of pixels and colors where metadata isn't embed.

Seed and message length can be got from the [result](img/attach1.png). This is `b"\xed\xfe\xcb\x10"` and 34 (= 0x22). Furthermore, the pixels and colors where message is embed can be found because I know seed of randomization.

Finaly, I extracted bits from [image](out.png) by this [code](exploit.py) and concatnating them. I got the flag!!.

## Code

[here](exploit.py)

## Flag

`flag{4b50lu73ly_b4rb4r1c_1403379d}`
