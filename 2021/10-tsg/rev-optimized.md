_Author: Dronex_

コードが動的に展開されているようなので、readシステムコールのあたりで停止させ、メモリダンプを取って保存。

main関数らしきコードを読むと、次のようになっている。

- 32bitの符号なし整数を4つ読み込む。
- 各整数のそれぞれに対して、何やら計算を行ってチェックを行う。
- 全てのチェックが通ったらflagが表示される。

チェックは失敗した時点でエラーが表示され、4つの整数は独立してチェックされるため、一つ一つ順番に正解を特定できる。

一つ目の整数に対するチェックは次のようになっている。

```
        00400969 8b 4c 24 10     MOV        ECX,dword ptr [RSP + v0]
        0040096d 48 b8 17        MOV        RAX,0x5f50ddca7b17
                 7b ca dd 
                 50 5f 00 00
        00400977 48 0f af c1     IMUL       RAX,RCX
        0040097b ba 91 af        MOV        EDX,0x2af91
                 02 00
        00400980 48 f7 e2        MUL        RDX
        00400983 81 e2 ff        AND        EDX,0x3ffff
                 ff 03 00
        00400989 66 48 0f        MOVQ       XMM0,RDX
                 6e c2
        0040098e 66 0f 73        PSLLDQ     XMM0,0x8
                 f8 08
        00400993 b8 69 95        MOV        EAX,0x9569
                 00 00
        00400998 66 48 0f        MOVQ       XMM1,RAX
                 6e c8
        0040099d 66 0f 73        PSLLDQ     XMM1,0x8
                 f9 08
        004009a2 66 0f 74 c8     PCMPEQB    XMM1,XMM0
        004009a6 66 0f d7 c1     PMOVMSKB   EAX,XMM1
        004009aa 3d ff ff        CMP        EAX,0xffff
                 00 00
        004009af 0f 85 42        JNZ        LAB_00400bf7
                 02 00 00
        004009b5 48 b8 8f        MOV        RAX,0x4dc4591dac8f
                 ac 1d 59 
                 c4 4d 00 00
        004009bf 48 0f af c1     IMUL       RAX,RCX
        004009c3 ba b9 4a        MOV        EDX,0x34ab9
                 03 00
        004009c8 48 f7 e2        MUL        RDX
        004009cb 81 e2 ff        AND        EDX,0x3ffff
                 ff 03 00
        004009d1 66 48 0f        MOVQ       XMM0,RDX
                 6e c2
        004009d6 66 0f 73        PSLLDQ     XMM0,0x8
                 f8 08
        004009db b8 f2 6c        MOV        EAX,0x26cf2
                 02 00
        004009e0 66 48 0f        MOVQ       XMM1,RAX
                 6e c8
        004009e5 66 0f 73        PSLLDQ     XMM1,0x8
                 f9 08
        004009ea 66 0f 74 c8     PCMPEQB    XMM1,XMM0
        004009ee 66 0f d7 c1     PMOVMSKB   EAX,XMM1
        004009f2 3d ff ff        CMP        EAX,0xffff
                 00 00
        004009f7 0f 85 fa        JNZ        LAB_00400bf7
                 01 00 00
```

z3に投げると解が出てきた。このコードの後ろには残りの3つの整数についてのチェックが同じように並んでいるだけで、全てz3が解いてくれた。

772928896, 2204180909, 4273479145, 1334930147を入力することでflagが表示される。

## solver

```python
from __future__ import annotations
import z3

def to(s: int | z3.BitVecRef, ln: int) -> z3.BitVecRef:
    if isinstance(s, int):
        return z3.BitVecVal(s, ln)
    if s.size() < ln:
        return z3.ZeroExt(ln - s.size(), s)
    else:
        return z3.Extract(ln-1, 0, s)

u64 = lambda s: to(s, 64)
u32 = lambda s: to(s, 32)
u128 = lambda s: to(s, 128)

def solve_v0():
    s = z3.Solver()
    v0 = z3.BitVec("v0", 32)

    rcx = u64(v0)
    rax = u64(0x5f50ddca7b17)
    rax = rax * rcx
    rdx = u64(0x2af91)
    rdx = u64(z3.LShR((u128(rax) * u128(rdx)), 64))
    rdx &= 0x3ffff
    xmm0 = u128(rdx)
    xmm0 <<= 8
    rax = 0x9569
    xmm1 = u128(rax)
    xmm1 <<= 8

    s.add(xmm1 == xmm0)

    rax = u64(0x4dc4591dac8f)
    rax = u64(rax * rcx)
    rdx = u64(0x34ab9)
    rdx = u64(z3.LShR((u128(rax) * u128(rdx)), 64))
    rdx &= 0x3ffff
    xmm0 = u128(rdx)
    xmm0 <<= 8
    rax = 0x26cf2
    xmm1 = u128(rax)
    xmm1 <<= 8

    s.add(xmm1 == xmm0)

    if s.check() == z3.sat:
        m = s.model()
        print(m.eval(v0))
    else:
        print("UNSAT!")


def solve_v1():
    s = z3.Solver()
    v1 = z3.BitVec("v1", 32)

    rsi = u64(v1)
    rax = u64(0x4ae11552df1a)
    rax = rax * rsi
    rdx = 0x36b39
    rdx = u64(z3.LShR((u128(rax) * u128(rdx)), 64))
    rdx &= 0x3ffff
    xmm0 = u128(rdx)
    xmm0 <<= 8
    rax = 0x20468
    xmm1 = u128(rax)
    xmm1 <<= 8

    s.add(xmm1 == xmm0)

    rax = u64(0x46680b140eff)
    rax = u64(rax * rsi)
    rdx = u64(0x3a2d3)
    rdx = u64(z3.LShR((u128(rax) * u128(rdx)), 64))
    rdx &= 0x3ffff
    xmm0 = u128(rdx)
    xmm0 <<= 8
    rax = 0x3787a
    xmm1 = u128(rax)
    xmm1 <<= 8

    s.add(xmm1 == xmm0)

    if s.check() == z3.sat:
        m = s.model()
        print(m.eval(v1))
    else:
        print("UNSAT!")

def solve_v2():
    s = z3.Solver()
    v2 = z3.BitVec("v2", 32)

    rdi = u64(v2)
    rax = u64(0x4d935bbd3e0)
    rdx = rdi | 0
    rdx = (rdx * rax)
    s.add(z3.ULT(rdx, rax))

    rax = u64(0x66b9b431b9ed)
    rax = rax * rdi
    rdx = u64(0x27df9)

    rdx = u64(z3.LShR((u128(rax) * u128(rdx)), 64))
    rdx &= 0x3ffff
    xmm0 = u128(rdx)
    xmm0 <<= 8
    rax = 0x5563
    xmm1 = u128(rax)
    xmm1 <<= 8

    s.add(xmm1 == xmm0)

    if s.check() == z3.sat:
        m = s.model()
        print(m.eval(v2))
    else:
        print("UNSAT!")


def solve_v3():
    s = z3.Solver()
    v3 = z3.BitVec("v3", 32)

    rbx = u64(v3)
    rax = u64(0x1e5d2be81c5)
    rdx = rbx | 0
    rdx = (rdx * rax)
    s.add(z3.ULT(rdx, rax))

    rax = u64(0x448626500938)
    rax = rax * rbx
    rdx = u64(0x3bc65)

    rdx = u64(z3.LShR((u128(rax) * u128(rdx)), 64))
    rdx &= 0x3ffff
    xmm0 = u128(rdx)
    xmm0 <<= 8
    rax = 0x133e7
    xmm1 = u128(rax)
    xmm1 <<= 8

    s.add(xmm1 == xmm0)

    if s.check() == z3.sat:
        m = s.model()
        print(m.eval(v3))
    else:
        print("UNSAT!")

solve_v0()
solve_v1()
solve_v2()
solve_v3()
```