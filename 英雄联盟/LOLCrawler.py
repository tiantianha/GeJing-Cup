from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import time
import csv
import selenium
import pyautogui
import selenium.common.exceptions
from selenium.webdriver.support.ui import Select


# 输入账号密码
def passwd(driver, account, wd):
    # 登录frame
    WebDriverWait(driver, 20, 0.05).until(lambda x: x.find_element_by_xpath('//*[@id="loginIframe"]'))
    loginFrame = driver.find_element_by_xpath('//*[@id="loginIframe"]')
    driver.switch_to.frame(loginFrame)
    WebDriverWait(driver, 50, 0.05).until(lambda x: x.find_element_by_xpath('//*[@id="switcher_plogin"]'))
    driver.find_elements_by_xpath('//*[@id="switcher_plogin"]')[0].click()

    # 输入账号密码，并点击登录
    WebDriverWait(driver, 20, 0.05).until(lambda x: x.find_element_by_xpath('//*[@id="u"]'))
    driver.find_elements_by_xpath('//*[@id="u"]')[0].clear()
    driver.find_elements_by_xpath('//*[@id="u"]')[0].send_keys(account)
    driver.find_elements_by_xpath('//*[@id="p"]')[0].clear()
    driver.find_elements_by_xpath('//*[@id="p"]')[0].send_keys(wd)
    driver.find_elements_by_xpath('//*[@id="login_button"]')[0].click()


# 滑块 进入个人中心
def skip(driver):
    print('请手动滑动滑块,登录成功请输入0')
    p = int(input())
    if p == 0:
        select = Select(driver.find_elements_by_xpath('//*[@id="areaContentId_lol"]')[0])
        select.select_by_visible_text('影流 电信')   # 选择大区 '影流 电信'
        time.sleep(5)
        WebDriverWait(driver, 20, 0.05).until(lambda x: x.find_element_by_xpath('//*[@id="confirmButtonId_lol"]'))
        driver.find_elements_by_xpath('//*[@id="confirmButtonId_lol"]')[0].click()  # 点击确定
        time.sleep(5)
        WebDriverWait(driver, 20, 0.05).until(lambda x: x.find_element_by_xpath('/html/body/div[3]/div[5]/div[3]/a[2]'))
        driver.find_elements_by_xpath('/html/body/div[3]/div[5]/div[3]/a[2]')[0].click()  # 点击游戏信息
        time.sleep(10)


def main_process(driver):
    datas = []
    # 我的荣誉
    q = 0
    for i in range(10):
        q = q + 1
        path1 = '//*[@id="honorIconul"]/li[' + str(q) + ']/p'   # 构造荣誉名称的xpath，如“三杀”
        path2 = '//*[@id="honorIconul"]/li[' + str(q) + ']/span'  # 构造上面荣誉名称的次数的xpath，如“三杀47次”
        # print(path1, path2)
        WebDriverWait(driver, 20, 0.05).until(lambda x: x.find_element_by_xpath(path1))
        honer1 = driver.find_elements_by_xpath(path1)[0].text  # 三杀
        times1 = driver.find_elements_by_xpath(path2)[0].text  # 47次
        print(honer1, times1)

        path3 = '//*[@id="honorScore"]/li[' + str(q) + ']/span[1]'   # 构造最高得分的xpath，如“最高评分”
        path4 = '//*[@id="honorScore"]/li[' + str(q) + ']/span[2]'   # 构造上面最高得分对应的分数的xpath，如“最高得分16.7”
        # print(path3, path4)
        honer2 = driver.find_elements_by_xpath(path3)[0].text   # 最高评分
        scores2 = driver.find_elements_by_xpath(path4)[0].text  # 16.7
        print(honer2, scores2)


    # 历史战绩
    k = 0
    for j in range(15):
        for i in range(10):
            k = k + 1
            path_man = '//*[@id="indexHtml"]/div/div/div[2]/ul[2]/li[' + str(k) + ']/span[1]/a[2]'
            path_map = '//*[@id="indexHtml"]/div/div/div[2]/ul[2]/li[' + str(k) + ']/span[2]/a[1]'
            path_class = '//*[@id="indexHtml"]/div/div/div[2]/ul[2]/li[' + str(k) + ']/span[2]/a[2]'
            path_KDA = '//*[@id="indexHtml"]/div/div/div[2]/ul[2]/li[' + str(k) + ']/span[4]'
            path_eco = '//*[@id="indexHtml"]/div/div/div[2]/ul[2]/li[' + str(k) + ']/span[5]'
            path_date = '//*[@id="indexHtml"]/div/div/div[2]/ul[2]/li[' + str(k) + ']/span[6]'
            # print(path_man, path_map, path_class, path_KDA, path_eco, path_date)
            WebDriverWait(driver, 50, 0.05).until(lambda x: x.find_element_by_xpath(path_man))
            man = driver.find_elements_by_xpath(path_man)[0].text  # 英雄角色
            game_map = driver.find_elements_by_xpath(path_map)[0].text    # 召唤师峡谷
            game_class = driver.find_elements_by_xpath(path_class)[0].text  # 匹配
            KDA = driver.find_elements_by_xpath(path_KDA)[0].text   # 1/2/3
            economic = driver.find_elements_by_xpath(path_eco)[0].text  # 5.1k/79
            date = driver.find_elements_by_xpath(path_date)[0].text  # 2020-05-01 14:03
            print(man, game_map, game_class, KDA, economic, date)
            datas.append([man, game_map, game_class, KDA, economic, date])
        print('点击 浏览更多信息 中,休眠30s让其加载')
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')     # 鼠标向下滚动至 浏览更多信息 按钮
        driver.find_elements_by_xpath('//*[@id="loadGame_btn"]')[0].click()   # 点击“浏览更多信息”
        time.sleep(10)

    with open(r'F:\PYTHON\TEST\customer\微信\隔镜杯\王者荣耀\1.csv', 'a+') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(datas)


if __name__ == '__main__':
    print('请输入账号')
    account = input()
    print('请输入密码')
    wd = input()
    options = webdriver.ChromeOptions()
    options.add_argument(
        'user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"')
    webdriver = webdriver.Chrome(chrome_options=options)
    url = 'http://lol.qq.com/space/index.shtml'
    webdriver.get(url)
    passwd(webdriver, account, wd)
    skip(webdriver)
    main_process(webdriver)
































