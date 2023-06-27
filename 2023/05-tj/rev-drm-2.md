# TJCTF 2023 - rev - drm-2

After some reversing, we can understand that `drm_exe` can work when all of `drm.key`, `drm.nonce`, `enc_song.dat` are put in the same directory.
Running this, we noticed that some audio were played at the same time. Let's see the part of this with Ghidra.

```c
        while( true ) {
          uVar5 = (ulong)local_a90;
          uVar4 = FUN_00103cdc(local_a28);
          if (uVar4 <= uVar5) break;
          piVar3 = (int *)FUN_00103d00(local_a28,(long)local_a90);
          __src = (void *)FUN_00103ba8(local_a48,(long)*piVar3);
          memcpy(local_a60,__src,0x15824);
          decrypt(local_a08,local_a60,0x15824);
          if (*local_a60 != '\0') {
            play_sound(local_a60,0xac12);
          }
          local_a90 = local_a90 + 1;
        }
```

In this while loop, if `local_a60` doesn't equal to 0, `play_sound` is called.
I thought this hid the flag audio (?) and tried to modify this if statements. I changed it from `jz` (`74 17`) to `jnz` (`75 17`).

After that we can hear the different audio, where there exist high-piched voice (like Chip 'n Dale) with some beep sound.
I focused on beep sound and found that this was a morse code. I forcibly decode it by my ear.

```
- .--- -.-. - ..-. -... .-. .- -.-. -.- . - .. -.. --- -. .----. - .-.. .. -.- . - --- ... .. -. --. .---- ..... ....- ----. ----- ---.. ----. --... -.... ----.
```

`tjctf{idon'tliketosing1549089769}`
