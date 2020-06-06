# Meta Mountains [forensics]

- Score: 100
- Solves: 788

## Problem

An image is given:

![](mountains_hsctf.jpg)

## Solution

Only exiftool...

```fish
$ exiftool mountains_hsctf.jpg
... snip ...
Exif Byte Order                 : Little-endian (Intel, II)
Compression                     : JPEG (old-style)
Make                            : Canon
Camera Model Name               : part 1/3: flag{h1dd3n_w1th1n_
Orientation                     : Horizontal (normal)
X Resolution                    : 180
Y Resolution                    : 180
Resolution Unit                 : inches
Software                        : part 2/3: th3_m0unta1ns_
Modify Date                     : 2012:02:03 11:18:05
Artist                          : part 3/3: l13s_th3_m3tadata}
Y Cb Cr Positioning             : Centered
Exposure Time                   : 1/160
F Number                        : 13.0
... snip ...
```

I found three parts of the flag, and concatenated them.

## Flag

`flag{h1dd3n_w1th1n_th3_m0unta1ns_l13s_th3_m3tadata}`
