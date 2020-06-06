# Comments [forensics]

- Score: 100
- Solves: 495

## Problem

A zip file `Comments.zip` is given.

## Solution

Firstly, I exacted the given zip file.

```fish
$ unar Comments.zip
Comments.zip: Zip
  1.zip  (1310 B)... OK.
Successfully extracted to "./1.zip".
$ unar 1.zip
1.zip: Zip
  2.zip  (1149 B)... OK.
Successfully extracted to "./2.zip".
$ unar 2.zip
2.zip: Zip
  3.zip  (988 B)... OK.
Successfully extracted to "./3.zip".
$ unar 3.zip
3.zip: Zip
  4.zip  (827 B)... OK.
Successfully extracted to "./4.zip".
$ unar 4.zip
4.zip: Zip
  5.zip  (666 B)... OK.
Successfully extracted to "./5.zip".
$ unar 5.zip
5.zip: Zip
  6.zip  (505 B)... OK.
Successfully extracted to "./6.zip".
$ unar 6.zip
6.zip: Zip
  7.zip  (344 B)... OK.
Successfully extracted to "./7.zip".
$ unar 7.zip
7.zip: Zip
  8.zip  (183 B)... OK.
Successfully extracted to "./8.zip".
$ unar 8.zip
8.zip: Zip
  flag.txt  (16 B)... OK.
Successfully extracted to "./flag.txt".
$ cat flag.txt
No flag here. :(
```

Where is the flag? The problem title `Comments` is a hint.

```fish
$ ls *.zip | xargs -n1 unzip -l
Archive:  1.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
     1149  2020-05-26 02:17   2.zip
l
---------                     -------
     1149                     1 file
Archive:  2.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
      988  2020-05-26 02:17   3.zip
a
---------                     -------
      988                     1 file
Archive:  3.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
      827  2020-05-26 02:17   4.zip
g
---------                     -------
      827                     1 file
Archive:  4.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
      666  2020-05-26 02:17   5.zip
{
---------                     -------
      666                     1 file
Archive:  5.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
      505  2020-05-26 02:17   6.zip
4
---------                     -------
      505                     1 file
Archive:  6.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
      344  2020-05-26 02:17   7.zip
n
---------                     -------
      344                     1 file
Archive:  7.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
      183  2020-05-26 02:16   8.zip
6
---------                     -------
      183                     1 file
Archive:  8.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
       16  2020-05-26 02:13   flag.txt
}
---------                     -------
       16                     1 file
Archive:  Comments.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
     1310  2020-05-26 02:17   1.zip
f
---------                     -------
     1310                     1 file
```

## Flag

`flag{4n6}`
