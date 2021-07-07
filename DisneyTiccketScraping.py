from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import sys
import datetime
import signal
import os

# Seleniumをあらゆる環境で起動させるオプション
from urllib3.util import wait
options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--disable-extensions')
options.add_argument('--proxy-server="direct://"')
options.add_argument('--proxy-bypass-list=*')
options.add_argument('--start-maximized')

driber_path = "driver/chromedriver"
driver = webdriver.Chrome(executable_path=driber_path)

#ラインへ通知を送る関数
def line_ntfy(mess):
    url = "https://notify-api.line.me/api/notify"
    token = '<<              >>'
    headers = {"Authorization": "Bearer " + token}
    payload = {"message": str(mess)}
    requests.post(url, headers=headers, params=payload)
def line_ntfy_kakuninn(num):
    url = "https://notify-api.line.me/api/notify"
    token = '<<              >>'
    headers = {"Authorization": "Bearer " + token}
    payload = {"message":'調査回数  '+str(num)}
    requests.post(url, headers=headers, params=payload)

#販売中の場合の判定＆クリック関数.販売中であればNone,販売中でなければ「現在、販売していません」の要素を返す
def PssportJudgeAndCilck(day, when, notbuy_xpath, click_xpath):
    if len(driver.find_elements_by_xpath(notbuy_xpath)) > 0:
        NotBuyElement = driver.find_element_by_xpath(notbuy_xpath)
        if NotBuyElement.text != '現在、販売していません':
            line_ntfy('\n【緊急事態】\n４月'+day+'日'+when+'のチケット再販開始\n急いでとってください\n\
            https://reserve.tokyodisneyresort.jp/')
            driver.find_element_by_xpath(click_xpath).click()
            return None
        else:
            return NotBuyElement
    else:
        line_ntfy('\n【緊急事態】\n４月'+day+'日'+when+'のチケット再販開始\n急いでとってください\n\
        https://reserve.tokyodisneyresort.jp/')
        driver.find_element_by_xpath(click_xpath).click()
        return None

#しっかり待機させる関数
def wait():
    driver.implicitly_wait(20)
    WebDriverWait(driver, 2000).until(EC.invisibility_of_element_located((By.ID, 'loading_modal0overlay')))
    time.sleep(5)

#軽く待機させる関数
def waitShort():
    driver.implicitly_wait(20)
    WebDriverWait(driver, 2000).until(EC.invisibility_of_element_located((By.ID, 'loading_modal0overlay')))
    time.sleep(3)


##############本題#################

#起動
driver.get("https://reserve.tokyodisneyresort.jp/")
wait()

#ログインクリック
driver.find_element_by_xpath('//*[@id="header"]/div/ul[2]/li/a/img').click()
wait()

#ログイン
LoginId = driver.find_element_by_xpath('//*[@id="_userId"]')
LoginId.send_keys("<<              >>")
password = driver.find_element_by_xpath('//*[@id="_password"]')
password.send_keys("<<              >>")
driver.find_element_by_xpath('//*[@id="_loginConection"]/form/p/a/img').click()
wait()

#トラベルバッグクリック
driver.find_element_by_xpath('//*[@id="header"]/div/ul[3]/li[2]/a/img').click()
wait()

#チケットを追加するクリック
driver.find_element_by_xpath('//*[@id="dayTable"]/tbody/tr[1]/td/table/tbody/tr/td[2]/a').click()
wait()

# ＞クリック
driver.find_element_by_xpath('//*[@id="searchCalendar"]/div/div/ul/button[2]').click()
wait()

#調査回数をカウントする変数
RandNum1day = 1
SeaNum2day = 1

#繰り返し４月１日と４月２日をチェックする。販売中であればbreakしてその画面のままにする
while True:
    #４月１日
    wait()

    # 日付のクリック（ホバーしてクリック、１秒の待機）
    ActionHover = ActionChains(driver)
    ActionHover.move_to_element(driver.find_element_by_xpath(\
    '//*[@id="searchCalendar"]/div/div/ul/div/div/li[2]/div/table/tbody/tr[1]/td[4]/a')).perform()
    driver.find_element_by_xpath(\
    '//*[@id="searchCalendar"]/div/div/ul/div/div/li[2]/div/table/tbody/tr[1]/td[4]/a').click()
    waitShort()

    #「自宅でプリントアウト」のクリック
    driver.find_element_by_xpath('//*[@id="searchEticket"]').click()
    wait()

    #青四角クリックができればクリック、できなければ次のアクションへ
    Rand1dayElements = PssportJudgeAndCilck(1, '1day', '//*[@id="searchResultList"]/ul/li[1]/div/p[3]',\
    '//*[@id="searchResultList"]/ul/li[1]/div')
    Rand1030toElements = PssportJudgeAndCilck(1, '10:30-', '//*[@id="searchResultList"]/ul/li[2]/div/p[3]',\
    '//*[@id="searchResultList"]/ul/li[2]/div')
    RandNoontoElements = PssportJudgeAndCilck(1, '昼-', '//*[@id="searchResultList"]/ul/li[3]/div/p[3]', \
    '//*[@id="searchResultList"]/ul/li[3]/div')
    if Rand1dayElements==None or Rand1030toElements==None or RandNoontoElements==None:
        break

    #確認用出力
    RandNum1day += 1
    print('４月１日チケット売り切れ中  :', RandNum1day, "周目", datetime.datetime.now())
    print(Rand1dayElements.text, Rand1030toElements.text, RandNoontoElements.text)


    #４月２日
    wait()

    # 日付のクリック
    ActionHover = ActionChains(driver)
    ActionHover.move_to_element(driver.find_element_by_xpath(\
    '//*[@id="searchCalendar"]/div/div/ul/div/div/li[2]/div/table/tbody/tr[1]/td[5]/a')).perform()
    driver.find_element_by_xpath(\
    '//*[@id="searchCalendar"]/div/div/ul/div/div/li[2]/div/table/tbody/tr[1]/td[5]/a').click()
    waitShort()

    #「自宅でプリントアウト」のクリック
    driver.find_element_by_xpath('//*[@id="searchEticket"]').click()
    wait()

    # もしクリックができればクリックとライン通知
    Sea1dayElements = PssportJudgeAndCilck(2, '1day', '//*[@id="searchResultList"]/ul/li[1]/div/p[3]', \
    '//*[@id="searchResultList"]/ul/li[1]/div')
    Sea1030toElements = PssportJudgeAndCilck(2, '10:30-', '//*[@id="searchResultList"]/ul/li[2]/div/p[3]', \
    '//*[@id="searchResultList"]/ul/li[2]/div')
    SeaNoontoElements = PssportJudgeAndCilck(2, '昼-', '//*[@id="searchResultList"]/ul/li[3]/div/p[3]', \
    '//*[@id="searchResultList"]/ul/li[3]/div')
    if Sea1dayElements == None or Sea1030toElements == None or SeaNoontoElements == None:
        break

    # 確認用出力
    SeaNum2day += 1
    print('４月２日チケット売り切れ中  :', SeaNum2day, "周目", datetime.datetime.now())
    print(Sea1dayElements.text, Sea1030toElements.text, SeaNoontoElements.text)

    # 確認用出力総合
    if(SeaNum2day%5 == 0):
        line_ntfy_kakuninn(SeaNum2day*2)