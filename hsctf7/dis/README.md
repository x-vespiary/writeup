# dis

## Writeup

In this challenge, we are given the file named "[disas](disas)". This file is disassembled code of pyc (maybe using "dis" module). I know the decompiler for pyc to python code(.py), so at first I searched assembler and aim to decompile assembled code.  
But I couldn't find such tools. And at some writeups of pyc challenges, they decompiled it by hand. So I decided to decompile by hand too, and I refer to [this page](https://docs.python.org/3/library/dis.html#python-bytecode-instructions) for decompilation.

### pyc

`pyc` is designed for stack machine, so some operaions push or pop value. For example, `LOAD_CONST 1 (0)` is the operation that `0` are pushed (`1` is identifer and means `co_consts[1]`. At this example, `co_consts[1] = 0`). `STORE_FAST 2 (i)` is the operation that the value of stack top is assigned to `i` (`2` is identifer and means `co_varnames[2]`. At this example, `co_varnames[2] = i`). But `STORE` operation is not pop operation. TOS(the top of the stack) is not poped.

Fucntion call uses stack. `CALL_FUNCTION (<num>)` operation pops `<num>` values and calls TOS (expected a reference to a function). For example, this operations call `len(s)`.

```
LOAD_GLOBAL              0 (len)
LOAD_FAST                0 (s)
CALL_FUNCTION            1
```

Code of list comprehension are compiled to a code object that returns list. In this object, empty list is created at first. Second, an iteration is started. At this iteration, values are calculated and appended to the list. Finaly, the list is retured.  
In "[disas](disas)", code objects of list comprehension correspond to line 63, 104 and 116.

The code of Generator uses `YIELD_VALUE` operation that pops and yields TOS.  
In "[disas](disas)", generator `b` uses this.

### decompilation

Result of decompilation is [here](decompile.py).  
In this code, input string is assigned to `s` and `s` is compared to `o` (`= b'\xae\xc0\xa1\xab\xef\x15\xd8\xca\x18\xc6\xab\x17\x93\xa8\x11\xd7\x18\x15\xd7\x17\xbd\x9a\xc0\xe9\x93\x11\xa7\x04\xa1\x1c\x1c\xed'`).  
At function `e`, `o[i] = b(a(s), c(s))[i]`. So I wrote the [code](exploit.py) making dictionary that maps bytes in `o` to printable charactors.  
Finaly, I concatenated charactors and got the flag!!.

## code

[here](exploit.py)

## Flag

`flag{5tr4ng3_d1s45s3mbly_1c0a88}`

## Resource

- <https://docs.python.org/3/library/dis.html#python-bytecode-instructions
