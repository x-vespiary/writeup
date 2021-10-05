# TSG CTF 2021: Advanced Fisher (Misc 365)

問題文にTSG LIVE CTF 6で出題された「Fisher」の派生問題だと書いてあるからまずはFisherを見る。

## 前提: Fisher
概要: Wavファイルにエンコードされたフラグをデコードする問題。ただしフレームはシャッフルされている。

### Encode
フラグ文字列を`0`と`1`で表したモールス信号列`signals`に変換する。
Wavファイルの`i`番目のフレームは`signals`の`i//2000`番目の要素が`0`であれば`0.0`、`1`であれば`np.sin(i * 439.97 / 44100 * (2 * np.pi)`とする。
ただしファイルを出力する前にフレームをランダムにシャッフルする。サンプルレートは44100でPCMは24bit。モジュールはsoundfileを使用。

### Decode
`f(i) = np.sin(i * 439.97 / 44100 * (2 * np.pi)`は今回の`i`の範囲であれば`i`と`f(i)`が一対一に対応するから、あり得る全ての`i`に対して実際に`f(i)`を計算して、エンコードされたWavファイルのフレームに存在するか比較すれば良い。

## Advanced Fisher
Advanced Fisherでは上記`f(i) = np.sin(i * 439.97 / 44100 * (2 * np.pi)`が`f(i) = np.sin(i * 440 / 44100 * (2 * np.pi)`に変わった問題である。`439.97`が`440`に変わったことで`i`と`f(i)`が一対一に対応しなくなる。具体的には`gcd(440, 44100) = 20`で`i * 440 / 44100 = i * 22 / 2205`であるから`f(i) = f(i + 2205)`になり`2205`個ごとに値が循環する。`i`と`f(i)`が一対一に対応しないため`signals[i//2000] = 1`である`i//2000`を特定できずFisherと同じようにデコードはできない。

今回のデコードで利用できそうな性質は`signals`の`k`番目の要素が`1`であれば、Wavファイルのフレームに`f(2000 * k)`, `f(2000 * k + 1)`, ... , `f(2000 * k + 1999)`が含まれていることである。例え`f(i)`のとりうる値が`2205`種類しかなくても各種類の出現数がわかればその区間被覆から逆算できる。各種類の出現数列の階差数列を求め、正である要素を貪欲に選択すればよい。

コードは以下。
```py
import soundfile as sf
import numpy as np
from utils import signals_to_string, string_to_signals
import collections

result_frames, _ = sf.read("result.wav")
frames_len = len(result_frames)
signals_len = 473

# 実際にWavファイルに出力してsinの値を取り出すことで誤差を0にする。
wave = np.array([np.sin(i * 440 / 44100 * (2 * np.pi)) for i in range(frames_len)])
sf.write("base.wav", wave, 44100, "PCM_24")
base_frames, _ = sf.read("base.wav")

T = 2205
L = 2000

frame_to_t = {base_frames[t]: t for t in range(T)}

# 出現回数
counts = [0] * T
for frame in result_frames:
    assert frame in frame_to_t # 誤差があればエラー
    counts[frame_to_t[frame]] += 1
counts[0] %= L

# 出現回数の階差数列
count_diff = [counts[t] - counts[(t - 1 + T) % T] for t in range(T)]

interval_lefts = []
while True:
    update = False
    for i in range(0, len(count_diff)):
        if count_diff[i] > 0:
            right = (L + i) % T
            interval_lefts.append(i)
            count_diff[i] -= 1
            count_diff[right] += 1
            update = True
    if not update:
        break

# フラグの先頭と末尾の区間が被ってしまうが、先頭はわかっているため末尾が一意に定まる。
flag_head = "TSGCTF{"
flag_head_signals = string_to_signals(flag_head)
signals = []

for k in range(signals_len):
    left = k * 2000 % T
    if k < len(flag_head_signals):
        if flag_head_signals[k] == 1:
            signals.append(1)
            interval_lefts.remove(left)
        else:
            signals.append(0)
    else:
        if left in interval_lefts:
            signals.append(1)
            interval_lefts.remove(left)
        else:
            signals.append(0)

print(signals_to_string(signals))
```

`TSGCTF{THE-TRUE-F1SHERM4N-U53S-M0RSE-CODE}`