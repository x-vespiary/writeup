# Extremely Complex Challenge

### Problem Outline
以下が与えられる。
 - 楕円曲線 y^2 = x^3 + ax + b (mod p)
   - p = 404993569381
   - b = 54575449882
 - 生成元 G = (391109997465, 167359562362)
 - 公開鍵 nG = (209038982304, 168517698208)

秘密鍵 n はいくつか？

### Writeup
まず、楕円曲線の式に、b,Gを代入して、aは求まる。

あとは、Baby-step Giant-step により、n を求めることができる。

[楕円曲線上の離散対数問題に対するアプローチ（Baby-step giant-stepとPollard's rho algorithm） - sonickun.log](http://sonickun.hatenablog.com/entry/2017/01/12/194011)

この記事のソースコードを使った。

`if giant in baby:`が O(m) になってしまっているので、set を使って高速化する。


`flag{17683067357}`