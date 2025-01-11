# XML External Entity

## XXE とは

XML が提供する外部実体参照機能を悪用した脆弱性および攻撃手法

## XML 構文

- <!DOCTYPE>宣言
  - XML 文書のドキュメント型定義を指定
  - `<!DOCTYPE ルート要素名 [内部サブセット]>`
    - e.g. `<!DOCTYPE data [<!ENTITY var "hoge">]>`
- エンティティ宣言
  - 内部エンティティ: `<!ENTITY internalEntityName "hello, world">`
  - 外部エンティティ`<!ENTITY externalEntityName SYSTEM "file:///path/to/file.txt">`
- エンティティ参照
  - `&entityName;`
- CDATA セクション
  - タグ(<>)などのメタ的な意味を持つ記号を文字として解釈する
  - `<![CDATA[CDATAとして扱われる内容]]>`
- 外部サブセット
  - 内部サブセットにおいてエンティティ参照に基づく動的な外部エンティティ宣言はできない
  - 外部サブセットに切り出すことで XML データの検証方法次第でエンティティ参照を元にした動的な値のエンティティを宣言できる
    - Validationg Processor -> 不可能
    - Non-Validating Processor -> 可能
  - 例えば lxml ライブラリは標準で False なので可能

## Blind XXE

ユーザーの入力値がユーザーにレスポンスされない場合

- 内部エラー出力の活用
  - あらかじめ file 変数に URL を格納しておく
  - 外部サブセットで、URL エラーになるように外部エンティティを定義しつつ、file の内容を URL にも含めておく
  - エラー分に file の内容が invalid url として表示される
- ファイルデータの外部への送信
  - エラーも表示されない場合に使用
  - 外部サブセット内の外部エンティティ参照の URL のクエリパラメータに、取得したファイル情報を埋め込む
  - ただし制約あり(URL として適切な文字のみ含むこと、XML の実体参照とみなされるような文字列が含まれていないこと)

ただし以上の内容の細かい実装や制約は XML ライブラリや言語に依存する

## PHP と XXE

- php の場合は php ラッパーを使えば base64 エンコードなどの処理を挟むことができることがある
- expect ラッパーを使用することで任意コード実行も可能になる
  - `expect://ls`
