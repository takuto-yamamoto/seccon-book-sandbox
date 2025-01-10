# SQL インジェクション

## SELECT による攻撃

- UNION
  - SQL インジェクションが可能、 SQL 実行結果がユーザーに返却される場合
  - UNION で他テーブルをくっつけて返却することでデータを取得する
- Error ベース
  - SQL インジェクションが可能、SQL 実行エラーがユーザーに出力される場合
  - 意図的に SQL 分のエラーを引き起こし、エラー分の中に取得したいデータを出力させる
  - MySQL であれば ExtractValue や UpdateXML 関数の XPATH が使用できる
- Boolean ベース
  - SQL インジェクションが可能、SQL 実行結果はユーザーに返却されないが、SQL 実行結果に応じてレスポンスが変化する場合
  - 「取得したいデータの 1 文字目が A なら 1、違うなら 0」みたいなクエリを注入することでデータを取得する
  - data を substr して ascii で比較(A なら 65)し、IF で boolean 化
- Time ベース
  - SQL インジェクションが可能、SQL 実行結果がユーザーに返却されない場合
  - SLEEP 関数を仕込むことで、「取得したいデータの 1 文字目が A なら 1 秒待機、違うなら待機しない」という挙動を引き起こし、応答時間からデータを判断する

## INSERT/UPDATE による攻撃

こちらも基本的に SELECT と同様

サブクエリによる DB 自体のアップデートや Boolean ベース、Time ベースをを使用する

## ブラックボックスでの見つけ方

- DevTools や HTTP プロキシでパラメータを見つける
- 実際にどのようなクエリで制御されているかのあたりをつける
- シングルクオート(test')やダブルクオート(test")で入力してみる
  - SQL 実行エラーが返ってくる場合 -> インジェクション可能
  - SQL 実行エラーが返ってこない場合
    - サーバエラーが発生しているか(ステータスコードやレスポンス)
    - 振る舞いの確認(test', test, test", test'', test"", or 1=1, or 1=2...etc)
- UNION を挿入する場合は前方の SELECT 文とカラム数を一致させる必要がある
  - ORDER BY {N}(N 番目のカラムでソート)をエラーが出るまで繰り返す
- テーブル情報の取得
  - MySQL だと information_schema.tables テーブルに情報あり(columns テーブルも存在)
    - group_concat 関数で全行データを結合できる
    - `select group_concat(table_name) from information_schema.tables;`
