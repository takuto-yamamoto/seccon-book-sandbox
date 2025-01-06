# Web の基礎知識

## プロトコル

### HTTP

#### リクエストのフォーマット

| セクション         | 記載例                          |
| ------------------ | ------------------------------- |
| リクエストライン   | POST /ctf HTTP/1.1              |
| メッセージヘッダー | HOST: www.example.com<br>etc... |
| 空白行             |                                 |
| メッセージボディ   | key1=value1&key2=value2         |

#### リクエストヘッダー

- Host: リクエスト宛先サーバのホスト名とポート番号
- User-Agent: リクエストを生成したユーザーエージェントの情報(ブラウザ種別やバージョン)
- Accept: ユーザーエージェントが受け入れ可能なコンテンツタイプ
- Referer: リクエストを送信する直前に参照していたリソースの URI
- Content-Type: 何らかのエンティティをメッセージボディに含めたリクエストにおいて、そのエンティティのコンテンツタイプを表す(Content-Length はそのエンティティの文字列の長さ)
- Cookie: cookie 情報(セッション ID とか)を格納する

#### レスポンスヘッダー

- Server: リクエストを処理したサーバソフトウェアやバージョン
- Location: クライアントにリダイレクト先を指示する(301: permanently removed)
- Set-Cookie: cookie 情報を保存するようクライアントに指示する

- Cookie: Expires, Domain, Path, Max-Age, Secure, HttpOnly
- HTTPS 通信キャプチャの複合
  - キャプチャファイルを WireShark に読み込ませる
  - 環境設定のプロトコル設定で TLS を指定する
  - 適切な RSA 秘密鍵やプリマスタシークレットのログファイルを指定する
- CSS は基本的に攻撃の入り口とはならないが、CSS インジェクションが一部の方法で可能(後述)

## コンテンツ

### JavaScript

- HTML の要素にアクセスして read/write
- HTML の要素にイベントハンドラを設定し、当該要素に対するイベントが発生した際に特定の処理をトリガーする
- HTTP リクエストを送信して他のリソースの情報を取得する
- API
  - document API で web ページの要素を取得および制御可能
  - location API で Web ページの位置情報を取得および制御可能(e.g. location.href で URL)
- 任意の JS コードを注入できる場合は location を利用した攻撃が可能
  - 正当な Web サイトを訪れたユーザーを悪意ある Web サイトへと強制的にナビゲートさせる
  - 当該 Web ページ上で実行される JS から取得可能なデータを攻撃者のサーバへと送信させる
    - location を機密情報属性を含む URI で書き換える JS コードを注入する

### XML

- root 要素は 1 つだがそれ以外は自由にタグ形式で記述可能
- Document Type Definition により XML 内で変数宣言が可能
  - 外部の dtd ファイルを読み込むことができる

## クライアント

### curl

- オプション
  - v: verbose
  - H: リクエストヘッダの表示
  - X: メソッドの指定
  - d: データの指定
  - A: User-Agent の指定
  - e: Referer の指定
  - b: cookie の指定

## サーバとアプリケーション

### nginx

- ディレクティブとコンテキストを定義するためのブロック
- ディレクティブは設定値のキーバリュー
- コンテキスト(ブロック)はコンテキストに応じたディレクティブを含むセット
  - main, events, http, server, location コンテキストなど

```conf
user nginx;
worker_processes 1; # リクエスト処理するプロセス数
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid

events {
  worker_connections 1024; # リクエスト処理プロセスが処理可能な同時接続数
}

http {
  include /etc/nginx/mime.types; # mimeタイプの定義
  default_type application/octet-stream; # 一致しない場合はバイナリ
  log_format main '...';
  access_log /var/log/nginx/access.log;
  server {
    listen 192.168.0.1:80; # サーバとしてリッスンするURI
    location / {
      root /var/www/html; # ドキュメントルートのパス
    }
  }
}
```

### Web アプリケーション

- リクエストの受信方法
  - リクエストのメソッドやパスに応じた処理の振り分け
  - クエリ文字列の処理
  - コンテンツタイプに応じたリクエストボディー処理
- レスポンスの構築方法
  - テンプレートを用いた HTML の構築
  - 出力値のエスケープ処理
- データベースとの連携方法
  - Web アプリケーションと DB の接続
  - SQL や ORM を用いた DB 上のデータの取得および更新

## データベース

### SELECT

```sql
SELECT [column1, column2, ...] FROM [table_name]
WHERE [condition] ORDER BY [column_name] LIMIT [num];
```

- condition 句で利用可能な条件式
  - column の値が A ではない(標準 SQL): column <> A
  - column の値が A ではない(MySQL): column != A
  - column の値が 1, 2, ...に含まれる: column IN (1, 2, ...)
- その他
  - JOIN: 内部結合/外部結合/交差結合
    - 内部結合: 共通する項目のみ結合
    - 外部結合: 片方に存在する項目のみ結合
    - 交差結合: 2 つのテーブルに存在する項目の全てを結合
  - UNION: 和結合
    - 和結合: 行方向の結合(UNION ALL で重複あり)
    - カラム数は同一である必要がある

### CASE

```sql
SELECT CASE WHEN [condition] THEN [value1]
ELSE [value2] END...
```

### サブクエリ

```sql
SELECT ... FROM ... WHERE external_id IN (SELECT id FROM ...);
```

### 関数

- COUNT, SUM, AVG, MAX, MIN, ...
- GROUP_CONCAT: 指定したカラムの値を指定したセパレータで結合する
- ASCII: 指定した文字の ASCII コードを返す
- SUBSTR: 指定した文字列の一部を切り出す
- TIMESTAMP: 文字列日付/時間を DATETIME/DATE に変換する
- SLEEP

## Web ブラウザのセキュリティ

- 機密情報を含んだコンテンツを JS プログラムから読み込むことができる場合に問題
- SameOrigin ポリシー
  - SameOrigin: スキーマ/ドメイン/ポート番号が同じ URI
  - SameOrigin であれば読み込みを許可
- CORS による SOP の緩和
  - CrossOrigin リクエストについてはリクエストヘッダに Origin ヘッダを付与
  - サーバは Access-Control-Allow-Origin ヘッダに許可する Origin を記載してレスポンス
  - ブラウザは ACAO ヘッダに Origin が含まれている場合にコンテンツの読み取りを許可する
  - プリフライトで CORS を満たしているかをチェックする
    - Access-Control-Allow-Methods
    - Access-Control-Allow-Headers
    - Access-Control-Expose-Headers: JS プログラムに Expose するヘッダ
    - Access-Control-Max-Age: プリフライトのレスポンスキャッシュ時間
    - Access-Control-Allow-Credentials: 本来のリクエストに資格情報を載せてもいいか
