# Pythagorean Tree Fractal 2 [algo]

- Score: 100
- Solves: 479

## Problem

See [PTF.pdf](PTF.pdf)

## Solution

Let $x := 70368744177664$.

The answer is $\sum_{i=1}^{25} x \cdot 2^{i-1} \cdot 2^{i-1} = 25x$.

```fish
$ python -c "print(25 * 70368744177664)"
1759218604441600
```

## Flag

`flag{1759218604441600}`
