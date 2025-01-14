# 使えそうなツール/アプリ

## Web

- burp suite
  - http プロキシ
- netcat
  - `nc [hostname] [port]`
    - 指定したホストとポートとの TCP 接続を開く
    - ヒアドキュメントやファイルを入力(`<<`や`<`)すれば HTTP リクエストやファイルの受け渡しが可能
  - `nc -l [port]`
    - 指定したポートでリッスン
- nmap
  - ポートスキャナ
- python
  - サーバ側の実装やスクリプトの作成に多用される
- curl
  - url リクエストツール
- SQLi チートシート類
  - [PortSwigger](https://portswigger.net/web-security/sql-injection/cheat-sheet)
  - [invicti](https://www.invicti.com/blog/web-security/sql-injection-cheat-sheet/)
  - HackTricks
- https://jwt.io
  - jwt のエンコード/デコード
- https://github.com/ticarpi/jwt_tool
  - jwt の改ざんや既知の攻撃

## Crypto

- quipquip
  - 単一換字暗号の自動解析
- https://gchq.github.io/CyberChef/
  - 暗号解読からハッシュ、バイナリ操作まで何でもできる
  - QR や Exif にも対応
- 難解プログラミング言語(esolang)
  - brainfuck
    - 難解プログラミング言語(esolang)
    - `<>+-.,[]`の 8 文字でポインタを操作しながら実装する
  - whitespace
    - ` `, `\t`, `\n`のみで構成される言語
  - piet
    - ドットでコーディングする(抽象画みたいになる)
  - lazy k
    - S, K と()だけで実装される関数型言語(ショートカットとして I も登場する)
  - JSFuck
    - `!+()[]`のみで動く難読化 JS
  - jjendoce/decode
    - js の難読化とそのデコード
- bkcrack
  - zip ファイルの既知平文攻撃

## Forensics

- wireshark
  - パケットキャプチャ
