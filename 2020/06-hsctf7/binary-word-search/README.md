# Binary Word Search [misc]

- Score: 223
- Solves: 126

## Problem

An image is given:

![](BinaryWordSearch.png)

- 0 is black, 1 is white.
- The entire flag is hidden, including flag{}.
- The flag may also be backwards or diagonally hidden.

## Solution

I implemented the solver to search the binary word whose prefix is `flag{`. This program searches horizontally, vertically, and diagonally, starting at each point.

- [solver.py](solver.py)

The result is as follows:

```fish
$ python solver.py
102: f
108: l
97: a
103: g
123: {
116: t
105: i
110: n
121: y
117: u
114: r
108: l
46: .
99: c
111: o
109: m
47: /
121: y
57: 9
102: f
115: s
107: k
121: y
104: h
54: 6
125: }
224: à
183: ·
69: E
87: W
flag{tinyurl.com/y9fskyh6}à·EW
```

## Flag

`flag{tinyurl.com/y9fskyh6}`
