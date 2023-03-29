# LINE CTF 2023 - Pwn - Simple Blogger

PING message is handled by the function at 0x4025dc, which does the below:

- Verify the first 4 bytes of the body of the message is "PONG".
- Execute a SQL query `SELECT token FROM sess WHERE rowid == 1` and fetch the result.
- Send a PONG message.

The size of PONG message shuold be 4 bytes, but actually it will be the same as the request.

```x64
0x004026fb      488b45f0                   mov rax, qword [rbp - 0x10]
0x004026ff      c60001                     mov byte [rax], 1
0x00402702      488b45f0                   mov rax, qword [rbp - 0x10]
0x00402706      c6400100                   mov byte [rax + 1], 0
0x0040270a      488b5510                   mov rdx, qword [rbp + 0x10] ; read the body size of the request.
0x0040270e      488b45f0                   mov rax, qword [rbp - 0x10]
0x00402712      48895008                   mov qword [rax + 8], rdx
0x00402716      488b45f0                   mov rax, qword [rbp - 0x10]
0x0040271a      488b5008                   mov rdx, qword [rax + 8]
0x0040271e      488b45f0                   mov rax, qword [rbp - 0x10]
0x00402722      488d4810                   lea rcx, [rax + 0x10]
0x00402726      488d45c0                   lea rax, [rbp - 0x40]
0x0040272a      4889c6                     mov rsi, rax
0x0040272d      4889cf                     mov rdi, rcx
0x00402730      e81beaffff                 call sym.imp.memcpy ; copy n bytes starting with "PONG" to the response message.
```

If the size is larger than 4 bytes, `memcpy` will copy not only "PONG" but also the following memory contents.
Therefore, if the size is large enough, the response will contain the result of the SQL query that is the token of admin session.

We can use this token to request "show the flag" function.

Flag: `LINECTF{2b9598e3eca50122436702e10877cdce}`
