# 使い方

## クーポンコードCSVの作成は以下の手順で行う

1. コマンドラインで main.py を実行する
2. コマンドライン引数として以下の引数がある
   - `-i` カスタムプライスにするかどうか。指定しないとベストプライス。
   - `-d` クーポン開始日 `yyyy-mm-dd` (省略で当日) (日本時間で入力)
   - `-t` クーポン開始時刻 `HH:MM` (省略で現在時刻) (日本時間で入力)
3. `coupon_file\couponcode.csv`が作成される
4. クリップボードにクーポンコードへのリンクが記載されたテキストがコピーされる
5. VSCodeなどでMarkDown形式ファイルを作成しブラウザに表示されるテキストをコピーする

(補足1) カスタムプライスで発行した場合、クーポンコードはコースID+連番、ベストプライスはuuidがクーポンコードになる。<br>
(補足2) `couponcode.csv`の内容でリダイレクト先を更新する。

## クーポンコードとプロモーションメール用の設定
- クーポン発行対象コースは `resources`ディレクトリの中にある`courses.csv`に記載する
- プロモーションメール用のテキストは `resources`ディレクトリの中にある`mail_template.txt`に以下のように記載する
- {}の中にはコースID+識別用コード、[]()のペアはリンク用の記述となる。

書式
```text
{コースID-name}
[リンク文字列](Udemyコースへのリンク/?couponCode={コースID-code})
```
例
```text
■{5238110-name}
[1200円クーポンで購入する ＞＞＞](https://www.udemy.com/course/python-engineer-basic/?couponCode={5238110-code})<br>
```
※ {}と[]()以外の文字列はそのまま出力される


## リダイレクト先(rebrandly.com)のURLを更新するには以下の手順で行う

1. コマンドラインで update_link.py を実行する
2. コマンドライン引数として以下の引数がある
   - `-b` ベストプライスにするかどうか。指定しないとカスタムプライス。
   - カスタムプライス用のURLとベストプライス用のURLの切替は、リダイレクトURLの title で行う
3. リダイレクト先のURLが更新される

カスタムプライス用URL切替は rebrandly api から返却される以下の書式のJSONで判定する

```json
{
   "29120f87f5c84dd4b5b5122818d75e5c": {
      "course_id": "5238110",
      "slashtag": "python-basic-bestprice",
      "course_link": "https://www.udemy.com/course/python-engineer-basic/",
      "title": "UdemyBestPrice"
   }
}
```

## rebrandly.comに新規URLを追加する手順

1. わかりやすい名前を付ける (slashtag)
2. `just a moment` の部分を `UdemyCustomPrice` に変える (title)
3. URLの`couponCode=???????`の`?`のコースIDを合わせる



## Udemyクーポンコード一括作成について

https://www.udemy.com/instructor/multiple-coupons-creation/
