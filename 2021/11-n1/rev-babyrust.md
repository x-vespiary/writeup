Rust's macro-based flag checker is given.
The input is converted into an array using the predefined rules of the macro.
The following code checks if the array of converted input and the array of converted flag match.

```rs
(@e ($Never:expr,$Gonna:expr,$Give:expr); (Never gonna give never gonna give)) => {
    let you = [148u8, 59, 143, 112, 121, 186, 106, 133, 55, 90, 164, 166, 167, 121, 174, 147, 148, 167, 99, 86, 81, 161, 151, 149, 132, 56, 88, 188, 141, 127, 151, 63];
    return $Never == you;
};
```

Insert `dbg!(&$Never);` into the code above.
```rs
(@e ($Never:expr,$Gonna:expr,$Give:expr); (Never gonna give never gonna give)) => {
    let you = [148u8, 59, 143, 112, 121, 186, 106, 133, 55, 90, 164, 166, 167, 121, 174, 147, 148, 167, 99, 86, 81, 161, 151, 149, 132, 56, 88, 188, 141, 127, 151, 63];
    dbg!(&$Never);
    return $Never == you;
};
```

Input `012345678901234567890123456789012` and calculate backward from the difference.

```py
flag_never = [148, 59, 143, 112, 121, 186, 106, 133, 55, 90, 164, 166, 167, 121, 174, 147, 148, 167, 99, 86, 81, 161, 151, 149, 132, 56, 88, 188, 141, 127, 151, 63, ]
s = [ord(c) for c in "012345678901234567890123456789012"]
s_never = [131, 54, 126, 112, 122, 170, 95, 138, 58, 92, 163, 150, 167, 107, 157, 150, 148, 156, 85, 78, 60, 155, 135, 131, 119, 59, 75, 175, 141, 114, 146, 60, 50, ]

flag = "n1ctf{"
for a, b, c in zip(s, s_never, flag_never):
    flag += chr(a + (c - b))
flag += "}"
print(flag)
```

Flag: `n1ctf{A6C33EA2571A2AE26BFAE7BEA2CD8F54}`