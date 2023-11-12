# TSG CTF 2023 - pwn/BABA PWN GAME

## Solution

The goal is to solve the puzzle "hard.y". This puzzle is unsolvable in its initial state. So the first step is to change the initial state.

```c
  // *** Step 2. Load the stage ***
  printf("DIFFICULTY? (easy/hard)\n");
  int i;
  for (i = 0; i < 63; i++) {
    char c = fgetc(stdin);
    if (c == '\n') break;
    if (c == '/' || c == '~') return 1; // no path traversal
    state.stage_name[i] = c;
  }
  strcpy(&state.stage_name[i], ".y");

  FILE *fp = fopen(state.stage_name, "r");
```

If the input for difficulty is `"hard.y\0".ljust(62)` (or you can give 63 instead), `state.stage_name` becomes `"hard.y\0 ... \0"` and the last part `"\0"` (or `"y\0"`) overwrites `state.spawn_off`.

```c
struct GameState {
  // meta values
  char stage_name[64];
  unsigned short spawn_off;
  ...
} state;

```

Initial spawn position (original):

```
#########################   SIX
#6#X   X     X    X    X#   I S
###  X  X  X   X      * #   WIN
  #  X     XO X     X   #   ####
  #X    X XX    X ###########  #
  #   XX         H     O    XXX#
  # *            H          X*X#
  ################ O       O####
  #          # #@#          #
  #*     #   O # #   O      #
###X         #   #          #
#   XXXX###################O#
#      HH O O O O O O O XXXH#
#####** #O O O O O O O O#####
    #   # O O O O O O O #
    #####################  O
```

Initial spawn position (when `"\0"` overwrites it):

```
#########################   SIX
#6#X   X     X    X    X#   I S
###  X  X  X   X      * #   WIN
  #  X     XO X     X   #   ####
  #X    X XX    X ###########  #
  #   XX         H     O    XXX#
  # *            H          X*X#
  ################ O       O####
@ #          # # #          #
  #*     #   O # #   O      #
###X         #   #          #
#   XXXX###################O#
#      HH O O O O O O O XXXH#
#####** #O O O O O O O O#####
    #   # O O O O O O O #
    #####################  O
```

Notice that the player `@` is standing outside the wall. The left and right edges of the stage are connected because they are adjacent in memory. In other words, if you move left beyond the left edge, you will reach the rightmost cell one row down, and vice versa. The implementation code for movement does not take the map edges into account and allows this kind of movement.

After moving left:

```
#########################   SIX
#6#X   X     X    X    X#   I S
###  X  X  X   X      * #   WIN
  #  X     XO X     X   #   ####
  #X    X XX    X ###########  #
  #   XX         H     O    XXX#
  # *            H          X*X#
  ################ O       O####
  #          # # #          #
  #*     #   O # #   O      #  @
###X         #   #          #
#   XXXX###################O#
#      HH O O O O O O O XXXH#
#####** #O O O O O O O O#####
    #   # O O O O O O O #
    #####################  O
```


Additionary, the cells below the bottom edge overlap the rule definitions.

```c
  // stage data
  unsigned short stage[STAGE_H][STAGE_W];
  unsigned short is_push[CHR_NUM]; // you can push this object if you move into a cell with the object
  unsigned short is_stop[CHR_NUM]; // you cannot move into a cell with this object
  unsigned short is_you[CHR_NUM];  // you can controll this object with WASD keys
  unsigned short is_sink[CHR_NUM]; // all objects in a cell are destroyed when something come onto a cell with the object
  ...
```

So the rule changes if an object is moved to these cells.

For example, pushing `O` down enables `is_stop[12]` in the following case. This corresponds to the rule "v is stop".

```
#####** #O O O O O O O O#####
    #   # O O O O O O O #  @
    #####################  O
[  is_push     ][  is_stop     ]
[  is_you      ][  is_sink     ]
...
```

```
#####** #O O O O O O O O#####
    #   # O O O O O O O #
    #####################  @
[  is_push     ][  is_stop O   ]
[  is_you      ][  is_sink     ]
...
```

With rule modifications, this puzzle is no longer unsolvable.

## Exploit

```python
sc.after("easy/hard").sendline("hard.y\0".ljust(62))
sc.after(">").sendline("sassssssaaaaasdddddwdssddsddssssssaassssssdswddsddswwd")
```

## Flag

```
TSGCTF{IS_TEND_TO_BE_BABA_IS_YOU_CTF?}
```