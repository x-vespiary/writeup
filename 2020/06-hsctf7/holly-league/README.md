# Holly League [algo]

- Score: 458
- Solves: 50

## Problem

See [Holly_League.txt](Holly_League.txt).

## Solution

This problem is categorized as "stable marriage problem". Gale-Shapley algorithm is well known for solving it. To cut corners in implementation, I used a Python package [matching](https://github.com/daffidwilde/matching).

- Source code: [solver.py](solver.py)

```fish
$ python solver.py
Here's case 1!
437 65
... snip ...
Sam Cote
Franklyn Sheppard
Fabian Mcdowell
Bertha Leech
Erin Small

> Trent Fellows
Congrats, that's right!
Wow, you really know your matchings!
Take this flag and get the heck out.
flag{C0l13g3_4dm15510n5_4r3_n3v3r_t415_ch1ll}
```

## Flag

`flag{C0l13g3_4dm15510n5_4r3_n3v3r_t415_ch1ll}`
