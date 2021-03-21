# Investigation Continues

## Writeup

To tell the truth, I couldn't solve this challenge. After CTF, I solved this challenge referring to some writeup.

In this challenge, we have to analyse the same file as [investigation](../investigation/README.md) and gather 3 timestamps.

1. the last time Adam entered incorrect password
2. the last time `1.jpg` was opened
3. the last time Chrome launched via taskbar

### dump registries

At first, I extracted registry files by `dumpregistry` plugin. Executed command was `volatility -f windows.vmem --profile=Win7SP1x64 dumpregistry --dump-dir dump_reg/`

To analyze regs, I used RegRipper. Opening a registry file in RegRipper and selecting a registry type, the result of analysis of the registry is dumped as text.

### timestamp1: incorrect password

The result of SAM registry analysis shows target information.

```
Username        : Adam [1000]
Full Name       : 
User Comment    : 
Account Type    : Default Admin User
Last Login Date : Wed Jul 22 09:05:19 2020 Z
Pwd Reset Date  : Mon Jul 20 13:22:12 2020 Z
Pwd Fail Date   : Wed Jul 22 09:05:11 2020 Z
Login Count     : 11
  --> Normal user account
```

`Pwd Fail Date` is target timestamp: `Wed Jul 22 09:05:11 2020 Z`.

### timestamp2: open file

I searched information from ntuser registry and found.

```
Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs\.jpg
LastWrite Time Thu Jan  1 00:00:00 1970 (UTC)
MRUListEx = 0
  0 = 1.jpg
```

This result shows `Thu Jan  1 00:00:00 1970 (UTC)` is last update time but it is obviously wrong and I stacked here...

After CTF, I read some writeups and noticed the registry key is correct but value is wrong. So I tried `printkey` plugin.

```
volatility -f windows.vmem --profile=Win7SP1x64 printkey -K "Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs\.jpg"
Volatility Foundation Volatility Framework 2.6
Legend: (S) = Stable   (V) = Volatile

----------------------------
Registry: \??\C:\Users\Adam\ntuser.dat
Key name: .jpg (S)
Last updated: 2020-07-21 18:38:33 UTC+0000

Subkeys:

Values:
REG_BINARY    MRUListEx       : (S) 
0x00000000  00 00 00 00 ff ff ff ff                           ........
REG_BINARY    0               : (S) 
0x00000000  31 00 2e 00 6a 00 70 00 67 00 00 00 4c 00 32 00   1...j.p.g...L.2.
0x00000010  00 00 00 00 00 00 00 00 00 00 31 2e 6c 6e 6b 00   ..........1.lnk.
0x00000020  38 00 08 00 04 00 ef be 00 00 00 00 00 00 00 00   8...............
0x00000030  2a 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   *...............
0x00000040  00 00 00 00 00 00 00 00 00 00 31 00 2e 00 6c 00   ..........1...l.
0x00000050  6e 00 6b 00 00 00 14 00 00 00                     n.k.......
```

Found!! Target timestamp is `2020-07-21 18:38:33 UTC+0000`

### timestamp3: Chrome via taskbar

This part is the easiest at this challenge. I used `userassist` plugin like as [investigation](../investigation/README.md)

```
$ volatility -f windows.vmem --profile=Win7SP1x64 userassist | grep "TaskBar.*Chrome" -A 20
Volatility Foundation Volatility Framework 2.6
REG_BINARY    %APPDATA%\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar\Google Chrome.lnk : 
Count:          3
Focus Count:    0
Time Focused:   0:00:00.503000
Last updated:   2020-07-21 17:37:18 UTC+0000
Raw Data:
0x00000000  00 00 00 00 03 00 00 00 00 00 00 00 03 00 00 00   ................
0x00000010  00 00 80 bf 00 00 80 bf 00 00 80 bf 00 00 80 bf   ................
0x00000020  00 00 80 bf 00 00 80 bf 00 00 80 bf 00 00 80 bf   ................
0x00000030  00 00 80 bf 00 00 80 bf ff ff ff ff 10 54 ef 94   .............T..
0x00000040  85 5f d6 01 00 00 00 00                           ._......

REG_BINARY    %APPDATA%\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar\Windows Explorer.lnk : 
Count:          1
Focus Count:    0
Time Focused:   0:00:00.501000
Last updated:   2020-07-21 18:20:23 UTC+0000
Raw Data:
0x00000000  00 00 00 00 01 00 00 00 00 00 00 00 01 00 00 00   ................
0x00000010  00 00 80 bf 00 00 80 bf 00 00 80 bf 00 00 80 bf   ................
0x00000020  00 00 80 bf 00 00 80 bf 00 00 80 bf 00 00 80 bf   ................
```

Target timestamp is `2020-07-21 17:37:18 UTC+0000`

Finaly, I concatenate them and got the flag!!

## Flag

`inctf{22-07-2020_09:05:11_21-07-2020_18:38:33_21-07-2020_17:37:18}`
