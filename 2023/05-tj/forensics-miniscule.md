# TJCTF 2023 - forensics - miniscule

In this challenge, a broken image file `miniscule.png` was given.


The compession method was `1`, not `0`.
I checked the data format in `IDAT` chunk using `file` command:
```
$ file data
data: Zstandard compressed data (v0.8+), Dictionary ID: None
```

So, I converted the data from Zstandard to Zlib.

```python
import zlib
import os
import binascii

data = open("miniscule.png", "rb").read()

ihdr = data[8:33]
assert ihdr[4:8] == b"IHDR"
idat = data[33:33+12+0x03501c]
assert idat[4:8] == b"IDAT"
iend = data[33+12+0x03501c:]
assert len(iend) == 12 and iend[4:8] == b"IEND"

# compression method: 1 -> 0
ihdr_data = ihdr[:18] + b"\x00" + ihdr[19:-4]
ihdr_crc = bytes.fromhex(hex(binascii.crc32(ihdr_data[4:]))[2:].zfill(8))

open("idat_data.zst", "wb").write(idat[8:-4])

os.system("unzstd idat_data.zst")
idat_data = zlib.compress(open("idat_data", "rb").read())
idat_len = bytes.fromhex(hex(len(idat_data))[2:].zfill(8))
idat_crc = bytes.fromhex(hex(binascii.crc32(b"IDAT" + idat_data))[2:].zfill(8))

data2 = data[:8] + (ihdr_data + ihdr_crc) + (idat_len + b"IDAT" + idat_data + idat_crc) + iend
open("out.png", "wb").write(data2)
```

The `out.png` was a valid image file and included a flag string.

```
tjctf{zlib_compression_bad_9c8b342}
```
