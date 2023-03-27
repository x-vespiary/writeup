# Fishing

- Japanese ver: https://project-euphoria.dev/blog/40-line-ctf-2023/#fishing

This challenge is a crackme of PE (portable executable).

The decompiled code of main function by Ghidra is here.

```c
undefined8 FUN_1400020fa(void)

{
  bool bVar1;
  undefined7 extraout_var;
  undefined8 in_R8;
  undefined8 in_R9;
  DWORD DStack_11c;
  undefined auStack_118 [264];
  HANDLE pvStack_10;
  
  FUN_140002547();
  FUN_140003bd0(&DAT_1400060b1,"Wanna catch a fish? Gimme the flag first",in_R8,in_R9);
  FUN_140003b70("%255s",auStack_118,0x100,in_R9);
  pvStack_10 = CreateThread((LPSECURITY_ATTRIBUTES)0x0,0,(LPTHREAD_START_ROUTINE)&LAB_140001e2f,
                            auStack_118,4,&DStack_11c);
  if (pvStack_10 == (HANDLE)0x0) {
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  bVar1 = FUN_140002010(pvStack_10);
  if ((int)CONCAT71(extraout_var,bVar1) != 0) {
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  ResumeThread(pvStack_10);
  WaitForSingleObject(pvStack_10,0xffffffff);
  CloseHandle(pvStack_10);
  return 0;
}
```

After receiving the input, `LAB_140001e2f` is called (or jumped?).

The decompiled code of this is here.

```c
undefined8 UndefinedFunction_140001e2f(byte *param_1)

{
  int iVar1;
  size_t sVar2;
  undefined8 uStack_68;
  undefined8 uStack_60;
  undefined4 uStack_58;
  undefined8 uStack_48;
  undefined8 uStack_40;
  undefined8 uStack_38;
  undefined uStack_30;
  undefined7 uStack_2f;
  undefined uStack_28;
  undefined8 uStack_27;
  byte *pbStack_18;
  int iStack_c;
  
  uStack_48 = 0xb534f0bd5a9fbed0;
  uStack_40 = 0xd7aeba99e2fb6fd0;
  uStack_38 = 0x3b04522c22dd536;
  uStack_30 = 0x9d;
  uStack_2f = 0x2acc28c7536663;
  uStack_28 = 0x2b;
  uStack_27 = 0x3a4660e39b09bb14;
  uStack_68 = 0x4e505fa94f652223;
  uStack_60 = 0x5d3126355d2c2d5d;
  uStack_58 = 0x494d4d26;
  sVar2 = strlen((char *)param_1);
  iStack_c = (int)sVar2;
  pbStack_18 = (byte *)malloc((longlong)(iStack_c + 1));
  if (pbStack_18 == (byte *)0x0) {
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  memset(pbStack_18,0,(longlong)(iStack_c + 1));
  FUN_140001cdf((longlong)param_1,iStack_c);
  FUN_140001d33((longlong)param_1,iStack_c);
  FUN_140001d87((longlong)&uStack_68,0x14);
  FUN_140001ddb((longlong)&uStack_68,0x14);
  FUN_140002310(param_1,iStack_c,(byte *)&uStack_68,0x14,pbStack_18);
  if (iStack_c == 0x29) {
    iVar1 = memcmp(&uStack_48,pbStack_18,0x29);
    if (iVar1 == 0) {
      puts("Correct! You get a fish!");
      goto LAB_140001ff0;
    }
  }
  puts("Too bad! Not even a nibble...");
LAB_140001ff0:
  free(pbStack_18);
  return 0;
}
```

`param_1` is the input and converted to another array by `FUN_140001cdf` and `FUN_140001d33`. `uStack_68` is an array and converted to another array by `FUN_140001d87` and `FUN_140001ddb`.

These functions are so simple that we can emulate other languages (for example, Python), but somehow the results of emulation are different from actual results.

Fortunately, these functions convert array by one byte. So I extracted the array converted from `LINECTF{0123456789abcdef0123456789abcdef}` with using x64dbg and got the conversion table.

In addtion, `uStack_68` is constant value. So the converted value is also constant: `"m4g1KaRp_ON_7H3_Hook"`.

`FUN_140002310` is remained. The decompiled code is here. Some variables are renamed by me.

```c
void FUN_140002310(byte *inp,int inp_len,byte *key_l14,int const_14,byte *empty)

{
  byte box [258];
  byte local_16;
  byte local_15;
  int i;
  uint local_10;
  uint j;
  
  memset(box,0,0x100);
  create_SBOX_140002230(box,key_l14,const_14);
  j = 0;
  local_10 = 0;
  for (i = 0; i < inp_len; i = i + 1) {
    j = j + 1 & 0xff;
    local_10 = local_10 + box[j] & 0xff;
    local_15 = box[j];
    box[j] = box[local_10];
    box[local_10] = local_15;
    local_16 = box[(int)(uint)(byte)(box[local_10] + box[j])];
    empty[i] = inp[i] ^ box[(int)(uint)(byte)(box[local_10] + box[j])] ^ (char)local_10 - 0x18U;
  }
  return;
}
```

`create_SBOX_140002230` assigns the constant array to `box` (but maybe this is not SBOX). And `empty[i]` is assgined `inp[i] ^ local_16 ^ local_10 - 0x18`

After calling `FUN_140002310`, `uStack_48` and `empty` (pointed by `pbStack_18`) are compared. If these two values are same, the input is the flag.

The reversing step is simple.

1. reproduce `box`.
2. calculate correct `inp[i] := empty[i] ^ local_16 ^ local_10 - 0x18` using `box`
3. get the flag by using the convertion table of input

To get the flag, I wrote this code.

```python
key = b"m4g1KaRp_ON_7H3_Hook"
sbox = [i for i in range(0x100)]

local_10 = 0
for j in range(0x100):
    local_10 = key[j % 0x14] + sbox[j] + local_10
    local_10 &= 0xff
    sbox[j], sbox[local_10] = sbox[local_10], sbox[j]

line = ""
for i, c in enumerate(sbox):
    line += f"{c:02x} "
    if i % 16 == 15:
        line += "\n"


desired_inp = []
target = list(map(lambda x: int(x, 16), "D0 BE 9F 5A BD F0 34 B5 D0 6F FB E2 99 BA AE D7 36 D5 2D C2 22 45 B0 03 9D 63 66 53 C7 28 CC 2A 2B 14 BB 09 9B E3 60 46 3A".split()))

j = 0
local_10 = 0
for i in range(0x29):
    j += 1
    local_10 += sbox[j]
    local_10 &= 0xff
    sbox[j], sbox[local_10] = sbox[local_10], sbox[j]
    local_16 = sbox[(sbox[local_10] + sbox[j]) & 0xff]
    xored = local_16 ^ ((local_10 - 0x18) & 0xff)
    desired_inp.append(target[i] ^ xored)

inp = "LINECTF{0123456789abcdef0123456789abcdef}"
converted_inp = list(map(lambda x: int(x, 16),"49 21 59 01 F1 89 19 B0 66 5E 76 6E 86 7E 96 8E A6 9E E0 F8 F0 08 00 18 66 5E 76 6E 86 7E 96 8E A6 9E E0 F8 F0 08 00 18 C0".split()))

d = {}
for x,y in zip(inp, converted_inp):
    d[y] = x

flag = ""
for x in desired_inp:
    flag += d[x]

print(flag)
```

- flag: `LINECTF{e255cda25f1a8a634b31458d2ec405b6}`
