# 使い方

## クーポンコードCSVの作成は以下の手順で行う
1. コマンドラインで main.py を実行する
2. コマンドライン引数として以下の引数がある
   - -i カスタムプライスにするかどうか。指定しないとベストプライス。
   - -d クーポン開始日 (省略で当日)
   - -t クーポン開始時刻 (省略で現在時刻)
3. クーポンコードCSVが作成される

## リダイレクト先(rebrandly.com)のURLを更新するには以下の手順で行う
1. コマンドラインで update_link.py を実行する
2. コマンドライン引数として以下の引数がある
   - -i カスタムプライスにするかどうか。指定しないとベストプライス。
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
  },
}
```

## Udemyクーポンコード一括作成について

https://www.udemy.com/instructor/multiple-coupons-creation/
