# Aliens [algo]

- Score: 343
- Solves: 95

## Problem

There is a square of 500x500 cells, and each cell has an integer.  This problem is to find the sum of all subrectangles that sum to a number divisible by ​13.

## Solution

Let n be the size of 1 side of the square. We can solve this problem in O(n^4) time and O(n^2) space by using the cumulative sum of 2-dimensional array.

My source code is [here](solver.d).

```fish
$ rdmd solver.d < "Alien Marking.txt"
0
1
2
... snip ...
498
499
7508511543
```

## Flag

`flag{7508511543}`
