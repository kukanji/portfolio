from selenium import webdriver
import os, time
from bs4 import BeautifulSoup
import csv
import urllib
import re
import requests

#ウェブステのログイン情報を指定
login_url = 'https://mastersso.kanagawa-u.ac.jp/amserver/UI/Login?goto=https%3A%2F%2Fwebstation.kanagawa-u.ac.jp%3A443%2Fcampusweb%2Fportal.do%3Fpage%3Dmain'
user_id, password = (os.environ['ID'], os.environ['PASSWORD'])
#保存先フォルダ（絶対パスで指定）
save_dir = os.path.dirname(os.path.abspath(__file__))
save_file = save_dir + '/list.csv'
#Chromeのオプションで保存先フォルダを設定
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {
    'download.default_directory': save_dir})

#メイン処理
def login_download():
    #Chromeを起動
    driver = webdriver.Chrome(options = options)
    #ログイン処理実行
    try_login(driver)
    #掲示板に行く
    link_click(driver, 'menu-link-mt-kj')
    link_click(driver, 'menu-tab-dir2-1')
    link_click(driver, 'menu-link-mf-135062')
    html = driver.page_source
    time.sleep(2)
    print(html)
    driver.close()
    return html

#HTMLでデータを取得する                
def get_data(html):     
    load_url = "https://webstation.kanagawa-u.ac.jp/campusweb/"
    soup = BeautifulSoup(html, "html.parser")
    #aタグを取得
    table = soup.findAll("table", {"class":"normal auto-table-2 sp-table-none"})[0]
    rows = table.findAll("a")
    print(rows)
    # CSVデータを読み出す
    written_data = []
    with open("ku_info.csv", "r", encoding='utf-8') as f:
        reader = csv.reader(f)
        for list in reader:
            written_data.append(list)

    # 読みだしたデータ
    #CSVファイルを作成
    with open("ku_info.csv", "a", encoding='utf-8') as f:
        writer = csv.writer(f, lineterminator="\n")
        for row in rows:
            csvRow = []
            url = row.get("href")
            #URLを取得する
            link_url = urllib.parse.urljoin(load_url, url)
            #csvRowに絶対リンクがなかった時にリンクと文字列を追加してLINEに送信する
            flag = False
            for element in written_data:
                replaced_element1 = re.sub("_flowExecutionKey=.*?&", "", element[1])
                replaced_link_url = re.sub("_flowExecutionKey=.*?&", "", link_url)
                if element[0] == row.text and replaced_element1 == replaced_link_url:
                    flag = True
                    break
            # ファイルの中に同じものがなかった場合
            if flag == False:
                csvRow.append(row.text)
                csvRow.append(link_url)
                print(csvRow)
                #LINEにデータを送信する
                send_line(csvRow)
                print('ok')
                writer.writerow(csvRow)
            else:
                break

# ラインにメッセージを送信
def send_line(msg):
    # アクセストークンを以下に設定
    acc_token = 'hRlpZCPLF1gyEMOQUuqRgDGoFM7znrTWElcKuk0LiNt'
    url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': 'Bearer ' + acc_token}
    payload = {'message': msg}
    requests.post(url, headers = headers, params = payload)

#ログイン処理
def try_login(driver):
    #ログインページを開く
    driver.get(login_url)
    #ユーザー名とパスワードを書き込む
    usr = driver.find_element_by_name('IDToken1')
    usr.send_keys(user_id)
    pwd = driver.find_element_by_name('IDToken2')
    pwd.send_keys(password)
    submit = driver.find_element_by_xpath("//input[contains(@type, 'image')]")
    submit.click()

#ラベルを指定してリンクを検索しクリックする
def link_click(driver, label):
    a = driver.find_element_by_id(label)
    driver.execute_script("arguments[0].scrollIntoView(true);", a)
    a.click()     

if __name__ == '__main__':
    html = login_download()
    get_data(html)
    
    
