htmlのソースコードを見ると

```html
<h4>Anyways, the flag that you need for this cha<span class="blur">llenge is: <span
          class="poefKuKjNPojzLDf"></span></span></h4>
```

とあり、`poefKuKjNPojzLDf`が怪しい。CSSのソースコードを見に行くと

```css
.poefKuKjNPojzLDf:after {
	content: "f" "l" "a" "g" "{" "g" "l" "a" "s" "s" "e" "s" "_" "a" "r" "e" "_" "u" "s" "e" "f" "u" "l" "}" ;
}
```

と書いてあり、これがフラグ。

`flag{glasses_are_useful}`
