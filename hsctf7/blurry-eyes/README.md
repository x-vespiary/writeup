# Blurry Eyes [web]

- Score: 100
- Solves: 1193

## Solution

See HTML code:

```html
<h4>Anyways, the flag that you need for this cha<span class="blur">llenge is: <span
          class="poefKuKjNPojzLDf"></span></span></h4>
```

See CSS code:

```css
.poefKuKjNPojzLDf:after {
	content: "f" "l" "a" "g" "{" "g" "l" "a" "s" "s" "e" "s" "_" "a" "r" "e" "_" "u" "s" "e" "f" "u" "l" "}" ;
}
```

## Flag

`flag{glasses_are_useful}`
