# Investigation

## Writeup

This is my first memory dump analysis challenge.

### identify image profile

At first, I identified profile by `imageinfo` plugin.

```
$ volatility -f windows.vmem imageinfo
Volatility Foundation Volatility Framework 2.6
INFO    : volatility.debug    : Determining profile based on KDBG search...
          Suggested Profile(s) : Win7SP1x64, Win7SP0x64, Win2008R2SP0x64, Win2008R2SP1x64_23418, Win2008R2SP1x64, Win7SP1x64_23418
                     AS Layer1 : WindowsAMD64PagedMemory (Kernel AS)
                     AS Layer2 : FileAddressSpace (/mnt/c/share/CTF/InCTF2020/investigation/windows.vmem)
                      PAE type : No PAE
                           DTB : 0x187000L
                          KDBG : 0xf80002c560a0L
          Number of Processors : 1
     Image Type (Service Pack) : 1
                KPCR for CPU 0 : 0xfffff80002c57d00L
             KUSER_SHARED_DATA : 0xfffff78000000000L
           Image date and time : 2020-07-22 09:07:57 UTC+0000
     Image local date and time : 2020-07-22 14:37:57 +0530
```

The profile of this image is `Win7SP1x64`

### UserAssist

In this challenge, we have to identify the last time when windows calculator was run and the count Google Chrome run.

UserAssist records these info and we can see them from registry.

The registry key is
`HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist`.

Volatility has `userassist` plugin. This shows the results that userassist analysis.

I found these information from this plugin. The result is here.

```
$ volatility -f windows.vmem --profile=Win7SP1x64 userassist | grep calc -A 20
Volatility Foundation Volatility Framework 2.6
REG_BINARY    %windir%\system32\calc.exe : 
Count:          16
Focus Count:    29
Time Focused:   0:06:40.529000
Last updated:   2020-07-21 18:21:35 UTC+0000
Raw Data:
0x00000000  00 00 00 00 10 00 00 00 1d 00 00 00 9d 1a 06 00   ................
0x00000010  00 00 80 bf 00 00 80 bf 00 00 80 bf 00 00 80 bf   ................
0x00000020  00 00 80 bf 00 00 80 bf 00 00 80 bf 00 00 80 bf   ................
0x00000030  00 00 80 bf 00 00 80 bf ff ff ff ff b0 02 93 c4   ................
0x00000040  8b 5f d6 01 00 00 00 00                           ._......

REG_BINARY    Microsoft.Windows.StickyNotes : 
Count:          11
Focus Count:    15
Time Focused:   0:05:00.500000
Last updated:   2020-07-20 13:21:19 UTC+0000
Raw Data:
0x00000000  00 00 00 00 0b 00 00 00 0f 00 00 00 e0 93 04 00   ................
0x00000010  00 00 80 bf 00 00 80 bf 00 00 80 bf 00 00 80 bf   ................
0x00000020  00 00 80 bf 00 00 80 bf 00 00 80 bf 00 00 80 bf   ................
```

The last time is `2020-07-21 18:21:35 UTC+0000`.

```
$ volatility -f windows.vmem --profile=Win7SP1x64 userassist | grep Chrome -A 20
Volatility Foundation Volatility Framework 2.6
REG_BINARY    Chrome          : 
Count:          19
Focus Count:    25
Time Focused:   0:11:45.627000
Last updated:   2020-07-22 09:06:37 UTC+0000
Raw Data:
0x00000000  00 00 00 00 13 00 00 00 19 00 00 00 67 c2 0a 00   ............g...
0x00000010  00 00 80 bf 00 00 80 bf 00 00 80 bf 00 00 80 bf   ................
0x00000020  00 00 80 bf 00 00 80 bf 00 00 80 bf 00 00 80 bf   ................
0x00000030  00 00 80 bf 00 00 80 bf ff ff ff ff 50 b2 83 67   ............P..g
0x00000040  07 60 d6 01 00 00 00 00                           .`......

REG_BINARY    %windir%\explorer.exe : 
Count:          1
Focus Count:    4
Time Focused:   0:01:01.294000
Last updated:   2020-07-21 18:20:23 UTC+0000
Raw Data:
0x00000000  00 00 00 00 01 00 00 00 04 00 00 00 7a ed 00 00   ............z...
0x00000010  00 00 80 bf 00 00 80 bf 00 00 80 bf 00 00 80 bf   ................
0x00000020  00 00 80 bf 00 00 80 bf 00 00 80 bf 00 00 80 bf   ................
--
REG_BINARY    C:\Users\Public\Desktop\Google Chrome.lnk : 
Count:          16
Focus Count:    0
Time Focused:   0:00:00.516000
Last updated:   2020-07-22 09:06:37 UTC+0000
Raw Data:
0x00000000  00 00 00 00 10 00 00 00 00 00 00 00 10 00 00 00   ................
0x00000010  00 00 80 bf 00 00 80 bf 00 00 80 bf 00 00 80 bf   ................
0x00000020  00 00 80 bf 00 00 80 bf 00 00 80 bf 00 00 80 bf   ................
0x00000030  00 00 80 bf 00 00 80 bf ff ff ff ff 50 b2 83 67   ............P..g
0x00000040  07 60 d6 01 00 00 00 00                           .`......

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

The count is `19`.

I concatenate them and submit the flag!!

## Flag

`inctf{21-07-2020_18:21:35_19}`
