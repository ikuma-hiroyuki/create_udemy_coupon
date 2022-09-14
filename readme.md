# 使い方

1. create_udemy_coupon_csv.pyを実行
2. クーポン発行日は<code>2022/9/7 0:00(PST)</code>を基準に<code>基準 + 30日 * 発行回数</code>とする
4. course_id + 発行回数(4桁ゼロ埋め)でクーポンコード発行
5. 作られたcoupon_code.csvをアップロードする
6. udemy各コースのボーナスレクチャーのクーポンURLを修正する (前回値+1)



# 処理

1. udemy_coupon_code.csvを読込
   (当CSVを元にcoupon_codeとstart_dateを書き換えて、新たにcoupon_code.csvを作る)
2. 発行回数はudemy_coupon_code.csvの<code>start_date</code>(2022-09-07) - 実行日 // COUPEN_LIFESPAN + 1
3. coupen_code.csvのcoupon_code = course_id + 発行回数(4桁ゼロ埋め)
4. coupen_code.csvのstart_date = <code>start_date</code> + 30 * 発行回数
5. coupon_code.csv 格納ディレクトリをエクスプローラーで開く

# Udemyクーポンコード一括作成について
https://www.udemy.com/instructor/multiple-coupons-creation/
