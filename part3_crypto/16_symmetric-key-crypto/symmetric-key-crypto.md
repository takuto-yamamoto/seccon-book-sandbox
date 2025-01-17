# 共通鍵暗号

## 鍵暗号の種類

- DES
  - 鍵の長さが短いため危殆化
  - Feistel 構造
    - 暗号と複合で同じ回路を使用できる
    - FEAL や Camellia などでも採用されている
  - 鍵の長さを 3 倍にしたトリプル DES もある
- AES
  - DES の後継アルゴリズムで現在主流
  - SPN
- RC4
  - 危殆化したストリーム暗号
  - 鍵によって生成された内部状態と平文を逐次的に XOR することで暗号化
    - 逆に暗号文と内部状態を XOR すれば平文を複合可能
- ChaCha20
  - AES よりも高速かつシンプルなストリーム暗号

## パディング方式

- ブロック暗号は固定長のためパディングが必要
- PKCS#7 パディング
  - 1 ブロック 255 バイトまでの場合に使用可能
  - 不足するバイトが N バイトなら、値 N のバイト N 個をパディングする
  - ちょうどブロックの長さなら、ブロック長のパディング(各バイトは値がブロック長に等しい) を追加する
- ゼロパディング
  - 全て 0 で埋める
  - ちょうどブロックの長さの場合は何もしない

## 攻撃種類

- ビットフリップ攻撃
  - ストリーム暗号では平文と鍵(から生成される擬似乱数配列)を XOR することで暗号化を実施する
  - 暗号文のあるビットを反転させることで平文の同じ場所を反転させることができ、平文の値を書き換えられる
- ECB モードに対する攻撃
  - 平文ブロックと暗号文ブロックが 1 対 1 で紐づく
  - 暗号文ブロックを組み合わせて、特定の平文に対応する暗号文を作り出すことが可能
- パディングオラクル攻撃
  - CBC モードにおいて複合を行う場合に PKCS#7 パディングが不正であるというエラーが発生する場合に有効なテクニック