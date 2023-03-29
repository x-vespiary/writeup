# LINE CTF 2023 - Web - Adult Simple GoCurl

`redirectChecker` allows only one redirect if the original request destination is the challenge server itself.
Inspecting the source code of Gin, the framework used by the server, I found `redirectTrailingSlash` option. This option is enabled by default and allows a redirection to occur as below when conditions are met:
```go
func redirectTrailingSlash(c *Context) {
	req := c.Request
	p := req.URL.Path
	if prefix := path.Clean(c.Request.Header.Get("X-Forwarded-Prefix")); prefix != "." {
		prefix = regSafePrefix.ReplaceAllString(prefix, "")
		prefix = regRemoveRepeatedChar.ReplaceAllString(prefix, "/")

		p = prefix + "/" + req.URL.Path
	}
	req.URL.Path = p + "/"
	if length := len(p); length > 1 && p[length-1] == '/' {
		req.URL.Path = p[:length-1]
	}
	redirectRequest(c)
}
```

The value of `X-Forwarded-Prefix`  header will be inserted at the beginning of the redirect destination.
This redirect does not occur when the path is `/`, but somehow it does when the path is `//`.
Thus, a request to `//` with `X-Forwarded-Prefix` value of `/flag` will be redirected to `/flag/`.

Request: `/curl/?url=http%3A%2F%2F127.0.0.1%3A8080%2F%2F&header_key=X-Forwarded-Prefix&header_value=%2Fflag`

Flag: `LINECTF{b80233bef0ecfa0741f0d91269e203d4}`