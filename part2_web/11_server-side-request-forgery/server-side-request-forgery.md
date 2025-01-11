# server side request forgery

## SSRF とは

Web アプリケーションから任意の通信先に対して HTTP などのリクエストを送信可能な脆弱性およびその攻撃手法

## 例

- パブリックサーバ経由でプライベートサーバのデータを窃取する
  - Web アプリケーション A は外部に公開されており、内部ネットワークとも接続
  - 内部ネットワーク内に外部には公開されない Web アプリケーションが存在する
  - Web アプリケーション A は指定された任意の URL にアクセス・スクリーンショットの取得を行いユーザーに返却する機能をもつ
  - 攻撃者は内部ネットワーク内に存在する Web アプリケーションの URL を知っている

### 攻撃手法

- 手法 1: 通常の http
  - パブリックサーバからのみ redis への接続が受け付けられている
  - URL として redis エンドポイント(key=FLAG) を指定し、パブリックサーバにデータを取得させる
- 手法 2: libcurl で利用可能な Gopher プロトコルの利用
  - HTTP 以外のプロトコルに対しても柔軟なリクエストが送信可能なレガシープロトコル
  - gopher の形式
    - `gopher://<host>:<port>/<gopher-path>`
  - gopher-path の形式
    - `<gophertype><selector>`
    - `<gophertype><selector>%09<search>`
    - `<gophertype><selector>%09<search>%09<gopher+_string>`
  - gopher で http 通信
    - `curl gopher://localhost:8888/+GET%20/%20HTTP/1.1%0d%0aHost:%20localhost:8888%0d%0a%0d%0a`
- 手法 3: file スキームを利用したローカルファイルの読み込み

## ブラックボックスでの見つけ方

- Detect
  - URL を指定可能で、また Web アプリケーションないからそこにアクセスするような機能や箇所を探す
- Explore
  - localhost にアクセスさせてみる
  - アプリケーションのソースコード取得を試す
  - `file:///proc/self/cmdline`や`file:///proc/self/environ`
