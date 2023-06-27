# TJCTF 2023 - Rev - ily-df

While investigating the binary, I found a suspicious function at 0x229c, which erases rock blocks (L) recursively.

Using gdb to bypass the conditions for calling this function and executing it, the player fell to the lowest layer.
At the same time sand blocks (G) also fell, and they looked like some kind of pattern, so I dumped the memory to see the entire layer.

They turned out to represent the flag.

```
     GG   GGGGG   G       G G        G     G      GG   GGGGG   G        G G GG
   GG   G           G GGG  GGG G G     G GGG    GG   G           G GGG     GGG  GG
   GGGGGGGGGGGGGGGGGGGGG    G     G  GG     G   GGGGGGGGGGGGGGGGGGGGG         G GG
   G        GG                   GGGGG GG       G        GG            GGG  GG
   GG    GG               G       G G  GG G G   GG    GG                 G    GGGGG
   GGGGGGGGGGGGGGGGG      G   GG  G G  G    G   GGGGGGGGGGGGGGGGG          GG   GGG
         GG               GG     G GG  G GG G         GG                G GG GG GG
         GG       GG        G G     G  G              GG       GG          GG    G
      GGGGGGGGGGGGGG          G     G       G      GGGGGGGGGGGGGG      G  G G  G  G
         GG                 G    G    GG G GG         GG                 G  G G  G
         GGG     GGG        GG  GG   G  G GG          GGG     GGG        GGG  G   G
         GG       GG        G G     G       G         GG       GG      G G GG   G
         GGGGGGGGGGG        G G    GG GG  G           GGGGGGGGGGG        G G  G   G
            GGGGG               GG GG  GGGG G            GGGGG         G G   G  GG
    GGGG GGGGGGGGGGGGGGG   G  G  G GG   G        GGGG GGGGGGGGGGGGGGG    G    G   G
     GG   GGGGGGGGGGGGGGG  G    GG G G G G  G     GG   GGGGGGGGGGGGGGG GG        G
         GG       GG      GGG  G    GG  G  G          GG       GG        G   G G G
      GGGGGGGGGGGGGG      GG     G    G            GGGGGGGGGGGGGG       G GG  G   G

```
(Part of the layer, representing `tjctf{`)

Flag: `tjctf{i-L0v3-you-Dwarf-Fortre$s}`
