# 大学情報自動転送システム
神奈川大学掲示板から更新された新しい情報をラインに送信する
# 作成の動機
私の通っている大学では、ウェブサイトで更新された大学からの情報はOutlookなどのツールに転送されるようにできています。

しかし、一般的な大学生にとってはOutlookなどのツールは馴染みがなく忙しい時期などには大学から更新された情報を見落としてしまうことがあります。

大事な情報を見落としてしまうことで不利益や機会の損失などが発生してしまうのはとても残念なことです。

そこで、大学生に馴染みのあるLINEに大学からの新しい情報を送信することでこの問題を解決し、大学からの新しい情報の見逃し等を最小限に抑えることができます。
# システム構成
![ダイアグラム](system_structure.png)
## 矢印１
1.1　サイトにアクセス

1.2　ホームページにログインする

1.3　リンクをたどって掲示板のページまでいく
## 矢印２
2.1　掲示板のHTMLを解析する

2.2　掲示板の情報を抽出し、データを取得する

## 矢印３
3.1　CSVを読み出し、CSV内のデータを取得する

## 矢印４
4.1　掲示板から取得したデータとCSVから取得したデータが一致すればプログラムを終了する

4.2　掲示板から取得したデータとCSVから取得したデータが一致しなければCSVにデータを追加する

## 矢印５
5.1 CSVに新しく追加したデータをラインに転送する。
