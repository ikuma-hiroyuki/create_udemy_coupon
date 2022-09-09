# 使い方

1. create_udemy_coupon_csv.pyを実行
2. 何回目の発行か入力する
   2022/9/7 0:00(PST)を0回目とする
3. 作られたcoupon_code.csvをアップロードする



# 処理

1. udemy_coupon_code.csvを読込
   (当CSVを元にcoupon_codeとstart_dateを書き換えて、新たにcoupon_code.csvを作る)
2. coupon_code = course_id + 発行回数(4桁ゼロ埋め)
3. start_date = 2022-09-07 * 30 * 発行回数
4. coupon_code.csv 格納ディレクトリをエクスプローラーで開く
