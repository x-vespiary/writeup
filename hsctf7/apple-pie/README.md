# Apple Pie [misc]

- Score: 281
- Solves: 112

## Problem

```
Good luck reading this lol uDZD0 MDOD1 MA$ZF JDTD2 MDLDF5F*F1 MA$LF JEepbeepQ10 ZA$OF JC LA$TF JEepbeepQ02 ZA$OF JC LDWDF$LF+F1 MA$WF JDNDF13F*F70 MDNDF$NF+F1 MA$NF JA1 JDPD0 MDKD0 MEepbeepQ20 ZDPDF$PF+F1 MDKDF$KF+F1 MC LEepbeepQ22 ZDKDF$KF+F1 MC LDKDF$KF*F$PF MA$KF JA2 JA2 JDLDF$LF-F5 MA$LF JA$LF JDAD1 MDTD1 MEepbeepQ11 ZDPDF2F*F$AF MDPDF$PF+F1 MDTDF$TF+F$PF MDADF$AF+F1 MC LA$TF J!!!

The output will need to be converted to ascii characters.
Flag format: 'flag{'+output+'}'
```

## Solution

I found a page with Apple Pie esolang: https://esolangs.org/wiki/Apple_Pie.

1. Parse the given Apple Pie code into an AST by hand.
    - Result: [./input](input)
1. Implement the interpreter which inputs it.
    - Source code: [./interpreter.d](interpreter.d)
1. Execute:
    ```fish
    $ rdmd interpreter.d input
    051112116119048110052
    3ptw0n4
    ```

## Flag

`flag{3ptw0n4}`
