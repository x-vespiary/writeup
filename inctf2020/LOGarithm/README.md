# LOGarithm

## Writeup

In this challenge, I analysed memory dump and pcapng. This challenge is the most fun forensics challenges I tried ever!!

### Image profile

```
$ volatility -f Evidence.vmem imageinfo
Volatility Foundation Volatility Framework 2.6
INFO    : volatility.debug    : Determining profile based on KDBG search...
          Suggested Profile(s) : Win7SP1x64, Win7SP0x64, Win2008R2SP0x64, Win2008R2SP1x64_23418, Win2008R2SP1x64, Win7SP1x64_23418
                     AS Layer1 : WindowsAMD64PagedMemory (Kernel AS)
                     AS Layer2 : FileAddressSpace (/mnt/c/share/CTF/InCTF2020/logarithm/Evidence.vmem)
                      PAE type : No PAE
                           DTB : 0x187000L
                          KDBG : 0xf80002c070a0L
          Number of Processors : 1
     Image Type (Service Pack) : 1
                KPCR for CPU 0 : 0xfffff80002c08d00L
             KUSER_SHARED_DATA : 0xfffff78000000000L
           Image date and time : 2020-06-02 10:40:46 UTC+0000
     Image local date and time : 2020-06-02 16:10:46 +0530
```

Image profile is `Win7SP1x64`

### Process analysis

`pstree` plugin shows processes as tree structure. I searched suspicious processes and found `pythonw.exe` (PID is 2216).

```
$ volatility -f Evidence.vmem --profile Win7SP1x64 pstree
Volatility Foundation Volatility Framework 2.6
Name                                                  Pid   PPid   Thds   Hnds Time
-------------------------------------------------- ------ ------ ------ ------ ----
 0xfffffa8002d99b30:svchost.exe                       768    504      7    270 2020-06-02 10:36:15 UTC+0000
 0xfffffa80030b6500:dllhost.exe                      1796    504     17    198 2020-06-02 10:36:19 UTC+0000
 0xfffffa8002cef060:spoolsv.exe                      1160    504     13    264 2020-06-02 10:36:17 UTC+0000
 0xfffffa8002d42970:svchost.exe                       672    504     10    353 2020-06-02 10:36:15 UTC+0000
. 0xfffffa80030cbb30:WmiPrvSE.exe                    1764    672     10    202 2020-06-02 10:36:19 UTC+0000
. 0xfffffa8002b63500:WmiPrvSE.exe                    2280    672     11    292 2020-06-02 10:36:39 UTC+0000
 0xfffffa8002e7d350:vmtoolsd.exe                     1416    504     10    270 2020-06-02 10:36:18 UTC+0000
. 0xfffffa80021208d0:cmd.exe                         2556   1416      0 ------ 2020-06-02 10:40:46 UTC+0000
 0xfffffa8003214b30:svchost.exe                      2716    504     15    223 2020-06-02 10:36:55 UTC+0000
 0xfffffa80033e9060:SearchIndexer.                   2452    504     12    622 2020-06-02 10:36:45 UTC+0000
. 0xfffffa80038cd350:SearchProtocol                  2528   2452      8    282 2020-06-02 10:40:06 UTC+0000
. 0xfffffa800319fb30:SearchFilterHo                  3528   2452      6    101 2020-06-02 10:40:06 UTC+0000
 0xfffffa8002dccb30:svchost.exe                       816    504     21    475 2020-06-02 10:36:15 UTC+0000
. 0xfffffa8002eafb30:audiodg.exe                      288    816      7    131 2020-06-02 10:36:16 UTC+0000
 0xfffffa8002db9060:svchost.exe                      1204    504     20    307 2020-06-02 10:36:17 UTC+0000
 0xfffffa80031634a0:msdtc.exe                        1924    504     15    153 2020-06-02 10:36:19 UTC+0000
 0xfffffa8002e58b30:svchost.exe                       928    504     14    291 2020-06-02 10:36:16 UTC+0000
. 0xfffffa800328eb30:dwm.exe                          296    928      4     72 2020-06-02 10:36:38 UTC+0000
 0xfffffa80032943f0:sppsvc.exe                       3344    504      4    144 2020-06-02 10:38:19 UTC+0000
 0xfffffa8002e85b30:svchost.exe                       976    504     43    975 2020-06-02 10:36:16 UTC+0000
. 0xfffffa8002d3e060:taskeng.exe                     1172    976      5     79 2020-06-02 10:36:17 UTC+0000
 0xfffffa800335a060:WmiApSrv.exe                     3276    504      6    116 2020-06-02 10:38:44 UTC+0000
 0xfffffa8002ee1b30:svchost.exe                       344    504     24    659 2020-06-02 10:36:16 UTC+0000
. 0xfffffa80027e2060:wininit.exe                      412    344      3     74 2020-06-02 10:36:08 UTC+0000
.. 0xfffffa8002b51b30:lsm.exe                         528    412      9    144 2020-06-02 10:36:08 UTC+0000
.. 0xfffffa8002b60660:lsass.exe                       520    412      6    558 2020-06-02 10:36:08 UTC+0000
.. 0xfffffa8002b4a320:services.exe                    504    412     11    208 2020-06-02 10:36:08 UTC+0000
... 0xfffffa800327e060:taskhost.exe                  1372    504      9    146 2020-06-02 10:36:38 UTC+0000
... 0xfffffa8002d708e0:vmacthlp.exe                   736    504      4     53 2020-06-02 10:36:15 UTC+0000
... 0xfffffa8002dd4060:VGAuthService.                1380    504      4     84 2020-06-02 10:36:18 UTC+0000
... 0xfffffa8002cc2b30:svchost.exe                   1056    504     17    367 2020-06-02 10:36:17 UTC+0000
... 0xfffffa8002e14390:svchost.exe                   1500    504     13    337 2020-06-02 10:38:20 UTC+0000
. 0xfffffa80023eeb30:csrss.exe                        352    344      9    489 2020-06-02 10:36:08 UTC+0000
.. 0xfffffa8002fd1730:conhost.exe                    1288    352      0 ------ 2020-06-02 10:40:46 UTC+0000
 0xfffffa800327e060:taskhost.exe                     1372    504      9    146 2020-06-02 10:36:38 UTC+0000
WARNING : volatility.debug    : PID 1372 PPID 504 has already been seen
 0xfffffa8002d708e0:vmacthlp.exe                      736    504      4     53 2020-06-02 10:36:15 UTC+0000
WARNING : volatility.debug    : PID 736 PPID 504 has already been seen
 0xfffffa8002dd4060:VGAuthService.                   1380    504      4     84 2020-06-02 10:36:18 UTC+0000
WARNING : volatility.debug    : PID 1380 PPID 504 has already been seen
 0xfffffa8002cc2b30:svchost.exe                      1056    504     17    367 2020-06-02 10:36:17 UTC+0000
WARNING : volatility.debug    : PID 1056 PPID 504 has already been seen
 0xfffffa8002e14390:svchost.exe                      1500    504     13    337 2020-06-02 10:38:20 UTC+0000
WARNING : volatility.debug    : PID 1500 PPID 504 has already been seen
 0xfffffa8003011270:chrome.exe                       4032   2636     11    174 2020-06-02 10:37:31 UTC+0000
 0xfffffa8002fcb640:chrome.exe                       2648   2636      9     91 2020-06-02 10:36:55 UTC+0000
 0xfffffa8000e17b30:chrome.exe                       1284   2636      0 ------ 2020-06-02 10:38:55 UTC+0000
. 0xfffffa80032bc4a0:explorer.exe                    1100   1284     36    933 2020-06-02 10:36:38 UTC+0000
.. 0xfffffa80032feb30:vmtoolsd.exe                   2208   1100      8    182 2020-06-02 10:36:39 UTC+0000
.. 0xfffffa800347fb30:chrome.exe                     2636   1100     34    866 2020-06-02 10:36:55 UTC+0000
... 0xfffffa8002058930:chrome.exe                    3812   2636     13    188 2020-06-02 10:37:20 UTC+0000
... 0xfffffa8003141060:chrome.exe                    3124   2636     15    272 2020-06-02 10:37:08 UTC+0000
... 0xfffffa8000f52220:chrome.exe                    3480   2636     18    352 2020-06-02 10:37:14 UTC+0000
... 0xfffffa8000f8e3d0:chrome.exe                    3728   2636     17    306 2020-06-02 10:37:18 UTC+0000
... 0xfffffa8000de00f0:chrome.exe                    3424   2636      0 ------ 2020-06-02 10:37:13 UTC+0000
... 0xfffffa8003547060:chrome.exe                    2804   2636     10    235 2020-06-02 10:36:55 UTC+0000
... 0xfffffa8003549b30:chrome.exe                    2812   2636     16    324 2020-06-02 10:36:55 UTC+0000
.. 0xfffffa8000f48b30:cmd.exe                        3532   1100      1     19 2020-06-02 10:37:57 UTC+0000
.. 0xfffffa80030b0060:pythonw.exe                    2216   1100      3    163 2020-06-02 10:40:36 UTC+0000
 0xfffffa8002058930:chrome.exe                       3812   2636     13    188 2020-06-02 10:37:20 UTC+0000
WARNING : volatility.debug    : PID 3812 PPID 2636 has already been seen
 0xfffffa8003141060:chrome.exe                       3124   2636     15    272 2020-06-02 10:37:08 UTC+0000
WARNING : volatility.debug    : PID 3124 PPID 2636 has already been seen
 0xfffffa8000f52220:chrome.exe                       3480   2636     18    352 2020-06-02 10:37:14 UTC+0000
WARNING : volatility.debug    : PID 3480 PPID 2636 has already been seen
 0xfffffa8000f8e3d0:chrome.exe                       3728   2636     17    306 2020-06-02 10:37:18 UTC+0000
WARNING : volatility.debug    : PID 3728 PPID 2636 has already been seen
 0xfffffa8000de00f0:chrome.exe                       3424   2636      0 ------ 2020-06-02 10:37:13 UTC+0000
WARNING : volatility.debug    : PID 3424 PPID 2636 has already been seen
 0xfffffa8003547060:chrome.exe                       2804   2636     10    235 2020-06-02 10:36:55 UTC+0000
WARNING : volatility.debug    : PID 2804 PPID 2636 has already been seen
 0xfffffa8003549b30:chrome.exe                       2812   2636     16    324 2020-06-02 10:36:55 UTC+0000
WARNING : volatility.debug    : PID 2812 PPID 2636 has already been seen
 0xfffffa8000ca19e0:System                              4      0     96    621 2020-06-02 10:36:06 UTC+0000
. 0xfffffa8001c31310:smss.exe                         264      4      2     29 2020-06-02 10:36:06 UTC+0000
 0xfffffa8002808850:csrss.exe                         404    396     11    356 2020-06-02 10:36:08 UTC+0000
. 0xfffffa8000f2d060:conhost.exe                     3524    404      3     51 2020-06-02 10:37:57 UTC+0000
 0xfffffa8002b29810:winlogon.exe                      460    396      4    110 2020-06-02 10:36:08 UTC+0000
 0xfffffa8003479880:GoogleCrashHan                   2584   2128      6     90 2020-06-02 10:36:47 UTC+0000
 0xfffffa80033b9b30:GoogleCrashHan                   2576   2128      6    101 2020-06-02 10:36:47 UTC+0000
```

What command was executed at this process started? I used `cmdline` plugin.

```
$ volatility -f Evidence.vmem --profile Win7SP1x64 cmdline | grep pythonw.exe -n
Volatility Foundation Volatility Framework 2.6
158:pythonw.exe pid:   2216
159:Command line : "C:\Python27\pythonw.exe" "C:\Python27\Lib\idlelib\idle.pyw" -e "C:\Users\Mike\Downloads\keylogger.py"
```

Very very suspicious file was found!! I tried extracting `keylogger.py`.

### keylogger extraction

`filescan` and `dumpfiles` plugin were used to extract `keylogger.py`. At first, I identified the addresses the keylogger was loaded by this command.

```
$ volatility -f Evidence.vmem --profile Win7SP1x64 filescan | grep keylogger.py
Volatility Foundation Volatility Framework 2.6
0x000000003ee119b0     16      0 R--rwd \Device\HarddiskVolume1\Users\Mike\Downloads\keylogger.py
```

`0x000000003ee119b0` is the address. So we can extract file by this command (`volatility -f Evidence.vmem --profile Win7SP1x64 dumpfiles -D . -Q 0x3ee119b0 --name`).

The extracted keylogger is [here](./keylogger.py).

### keylogger analysis

I found some information from this keylogger.

1. This script records pushed keys until `esc` is pushed
2. The log is saved at `C:/Users/Mike/Desktop/key.log` but this file is deleted when log is sent to attacker(`18.140.60.203:1337`).
3. The log is encoded by base64 and xored the key that is `t3mp` environment variable.
4. Encoded log is sent.

In this challenge, we were given not only memory dump but also pcapng file. Filtering packets, I found the packets log was sent and extract data. The data was encoded by base64, so I decoded and saved as "[xored](./xored)"

### decode log

To decode log, we have to get key. Volatility has `envars` plugin that show environment variables.

```
$ volatility -f Evidence.vmem --profile Win7SP1x64 envars | grep pythonw.exe | grep t3mp
Volatility Foundation Volatility Framework 2.6
    2216 pythonw.exe          0x0000000000304d50 t3mp                           UXpwY1VIbDBhRzl1TWpkY08wTTZYRkI1ZEdodmJqSTNYRk5qY21sd2RITTdRenBjVjJsdVpHOTNjMXh6ZVhOMFpXMHpNanRET2x4WAphVzVrYjNkek8wTTZYRmRwYm1SdmQzTmNVM2x6ZEdWdE16SmNWMkpsYlR0RE9seFhhVzVrYjNkelhGTjVjM1JsYlRNeVhGZHBibVJ2CmQzTlFiM2RsY2xOb1pXeHNYSFl4TGpCY08wTTZYRkJ5YjJkeVlXMGdSbWxzWlhNZ0tIZzROaWxjVG0xaGNDNURUMDA3TGtWWVJUc3UKUWtGVU95NURUVVE3TGxaQ1V6c3VWa0pGT3k1S1V6c3VTbE5GT3k1WFUwWTdMbGRUU0RzdVRWTkQK
```

Ok, I got the [key](./key) and [encoded log](./xored), so I decoded log by [this code](./exploit.py). The result is here.

```
h a n g o  t s . g o o g l e . c o m h i Key.space d a v e . Key.space s e c r e t Key.space f l a g Key.space i n c t f Key.shift { n 3 v 3 r Key.shift _ Key.shift T r Key.shift U s 7 Key.shift _ Key.shift S p 4 m Key.shift _ e Key.shift _ m 4 1 Key.shift L s Key.shift } Key.esch a n g o  t s . g o o g l e . c o m h i Key.space d a v e . Key.space s e c r e t Key.space f l a g Key
```

There are some space and garbage. I deleted them and got the flag!!

## Flag

`inctf{n3v3r_TrUs7_Sp4m_e_m41Ls}`
