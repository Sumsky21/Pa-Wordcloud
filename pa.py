# 第三方库
import time
from urllib.parse import quote

import lxml
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By  # 指定 HTML 文件中 DOM 标签元素
from selenium.webdriver.support.ui import WebDriverWait  # 等待网页加载完成
from selenium.webdriver.support import expected_conditions as EC  # 指定等待网页加载结束条件
from selenium.webdriver.common.keys import Keys

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/78.0.3904.108 Safari/537.36'}
line = '\n----------------\n'


# 百度
def analyze_baidu(html, file):  # 分析页面源代码并提取文本
    h = BeautifulSoup(html, 'lxml')
    title = h.find_all('div', class_='c-abstract')  # 提取搜索结果中内容摘要对应的部分
    for item in title:
        file.write(item.get_text())  # 获取的文本输出至文件中
    file.write(line)


def pa_baidu(string, pagelen):  # 访问爬取页面并获得源代码
    brs = webdriver.Chrome()
    brs.get('https://www.baidu.com/')
    WebDriverWait(brs, 10).until(EC.presence_of_element_located((By.ID, "kw")))  # 等待网页加载完毕，10秒超时
    # 初次搜索并写入数据
    fbaidu = open('read.txt', 'w', encoding='utf-8')
    text = brs.find_element_by_id('kw')
    text.send_keys(string)
    time.sleep(0.2)
    search = brs.find_element_by_id('su')
    search.click()
    hcode = brs.page_source
    analyze_baidu(hcode, fbaidu)
    # 翻页循环搜索
    time.sleep(1)
    for i in range(eval(pagelen)):
        WebDriverWait(brs, 45).until(EC.visibility_of_element_located((By.LINK_TEXT, "下一页>")))
        nextpage = brs.find_element_by_link_text('下一页>')
        try:  # 在测试中这里的翻页不稳定，因此采用css选择器查找作为备用翻页按钮查找方式
            nextpage.click()
        except:
            time.sleep(0.3)
            nextpage = brs.find_element_by_css_selector('#page > a:nth-child(12)')
            nextpage.click()
        time.sleep(0.5)
        hcode = brs.page_source
        analyze_baidu(hcode, fbaidu)
    brs.close()


# 必应国内版
def analyze_bing(html, file):
    h = BeautifulSoup(html, 'lxml')
    title = h.find_all('p')
    for item in title:
        file.write(item.get_text())
    file.write(line)


def pa_bing(string, pagelen):
    brs = webdriver.Chrome()
    brs.get('https://cn.bing.com/search?q={}'.format(quote(string)))
    WebDriverWait(brs, 10).until(EC.presence_of_element_located((By.ID, "sb_form_q")))
    # 初次搜索并写入数据
    fbing = open('read.txt', 'w', encoding='utf-8')
    hcode = brs.page_source
    analyze_bing(hcode, fbing)
    # 翻页循环搜索
    time.sleep(0.5)
    j = 5
    for i in range(eval(pagelen)):
        if i == 0:
            j = 6
        elif i == 1:
            j = 8
        else:
            j = 9
        # 这是等待页面上翻页按钮加载出来，45秒后超时
        WebDriverWait(brs, 45).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#b_results > li.b_pag > nav '
                                                                                        '> ul > li:nth-child({}) > '
                                                                                        'a'.format(j))))
        nextpage = brs.find_element_by_css_selector('#b_results > li.b_pag > nav > ul > li:nth-child({}) > a'.format(j))
        nextpage.click()
        time.sleep(0.5)
        hcode = brs.page_source
        analyze_bing(hcode, fbing)
    brs.close()


# 谷歌
def analyze_google(html, file):
    h = BeautifulSoup(html, 'lxml')
    title = h.find_all('span', class_='st')
    for item in title:
        file.write(item.get_text())
    file.write(line)


def pa_google(string, pagelen):
    brs = webdriver.Chrome()
    brs.get('https://www.google.com.hk/')
    WebDriverWait(brs, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "Fx4vi")))
    # 初次搜索并写入数据
    fgoogle = open('read.txt', 'w', encoding='utf-8')
    text = brs.find_element_by_name('q')
    text.send_keys(string)
    time.sleep(0.2)
    text.send_keys(Keys.RETURN)  # 模拟输入回车
    # 检索关闭搜索结果省略
    if eval(pagelen) > 10:
        while 1:
            try:
                brs.find_element_by_link_text('下一页')
                n = brs.find_element_by_css_selector('#nav > tbody > tr > td:nth-child(11) > a')
                n.click()
            except:
                showall = brs.find_element_by_link_text('重新搜索以显示省略的结果')
                showall.click()
                break
    hcode = brs.page_source
    analyze_google(hcode, fgoogle)
    # 翻页循环搜索
    time.sleep(0.5)

    for i in range(eval(pagelen)):
        WebDriverWait(brs, 45).until(EC.visibility_of_element_located((By.LINK_TEXT, "下一页")))
        nextpage = brs.find_element_by_link_text('下一页')
        nextpage.click()
        time.sleep(0.5)
        hcode = brs.page_source
        analyze_google(hcode, fgoogle)
    brs.close()


# 微信公众平台
def analyze_weixin(html, file):
    h = BeautifulSoup(html, 'lxml')
    title = h.find_all('p', class_='txt-info')
    for item in title:
        file.write(item.get_text())
    file.write(line)


def pa_weixin(string, pagelen):
    print("微信搜索要求登录后才能查看完整的搜索结果。扫码登录是唯一的方式，这让我们无法在这一步实现自动化。\n请打开微信扫一扫界面，静待二维码出现！")
    brs = webdriver.Chrome()
    brs.get('https://weixin.sogou.com/')
    WebDriverWait(brs, 10).until(EC.presence_of_element_located((By.ID, "query")))
    # 初次搜索并写入数据
    fweixin = open('read.txt', 'w', encoding='utf-8')

    # 处理微信登录的问题
    try:
        login = brs.find_element_by_id('loginBtn')
        login.click()
    except:
        time.sleep(1)
        login = brs.find_element_by_id('loginBtn')
        login.click()
    print('请扫描二维码登录以继续。请在30秒内完成操作！')
    WebDriverWait(brs, 45).until(EC.visibility_of_element_located((By.CLASS_NAME, "yh")))  # 留时间在手机上操作

    text = brs.find_element_by_id('query')
    text.send_keys(string)
    time.sleep(0.2)
    search = brs.find_element_by_class_name('swz')
    search.click()
    hcode = brs.page_source
    analyze_weixin(hcode, fweixin)
    # 翻页循环搜索
    time.sleep(0.5)
    for i in range(eval(pagelen)):
        WebDriverWait(brs, 45).until(EC.visibility_of_element_located((By.CLASS_NAME, "np")))
        nextpage = brs.find_element_by_class_name('np')
        nextpage.click()
        time.sleep(0.5)
        hcode = brs.page_source
        analyze_weixin(hcode, fweixin)
    brs.close()


def analyze_weibo(html, file):
    h = BeautifulSoup(html, 'lxml')
    title = h.find_all('p', class_='txt')
    for item in title:
        file.write(item.get_text().replace('收起全文d', '').replace('展开全文c', '').replace('微博', '').replace('视频', ''))
    file.write(line)


# 微博
def pa_weibo(string, pagelen):
    print("微博搜索要求登录后才能查看完整的搜索结果。扫码登录是唯一的方式，这让我们无法在这一步实现自动化。\n请打开微博扫一扫界面，静待二维码出现！")
    brs = webdriver.Chrome()
    brs.get('https://weibo.com/')
    WebDriverWait(brs, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "gn_search_v2 ")))
    # 初次搜索并写入数据
    fweibo = open('read.txt', 'w', encoding='utf-8')

    # 处理登录的问题
    login = brs.find_element_by_link_text('安全登录')
    login.click()
    print('请扫描二维码登录以继续。请在30秒内完成操作！')
    # 留时间在手机上操作，检测到已经登录后继续下一步，45秒后超时
    WebDriverWait(brs, 45).until(EC.presence_of_element_located((By.CLASS_NAME, "nameBox")))

    text = brs.find_element_by_css_selector('#plc_top > div > div > div.gn_search_v2 > input')
    text.send_keys(string)
    time.sleep(0.2)
    search = brs.find_element_by_css_selector('#plc_top > div > div > div.gn_search_v2 > a')
    search.click()
    hcode = brs.page_source
    analyze_weibo(hcode, fweibo)
    # 翻页循环搜索
    time.sleep(0.5)
    for i in range(eval(pagelen)):
        WebDriverWait(brs, 45).until(EC.visibility_of_element_located((By.CLASS_NAME, "next")))
        nextpage = brs.find_element_by_class_name('next')
        nextpage.click()
        time.sleep(0.5)
        hcode = brs.page_source
        analyze_weibo(hcode, fweibo)
    brs.close()


def analyze_zhihu(html, file):
    h = BeautifulSoup(html, 'lxml')
    title = h.find_all('p', style="line-height:20px;padding:1px 0")
    for item in title:
        file.write(item.get_text().replace('更多>>', ''))
    file.write(line)


def pa_zhihu(string, pagelen):
    brs = webdriver.Chrome()
    brs.get('https://zhihu.sogou.com/')
    WebDriverWait(brs, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "sec-input")))
    # 初次搜索并写入数据
    fzhihu = open('read.txt', 'w', encoding='utf-8')

    text = brs.find_element_by_id('query')
    text.send_keys(string)
    time.sleep(0.2)
    text.send_keys(Keys.RETURN)
    hcode = brs.page_source
    analyze_zhihu(hcode, fzhihu)
    # 下拉搜索
    time.sleep(0.5)
    for i in range(eval(pagelen)):
        WebDriverWait(brs, 45).until(EC.visibility_of_element_located((By.CLASS_NAME, "np")))
        nextpage = brs.find_element_by_class_name('np')
        nextpage.click()
        time.sleep(0.5)
        hcode = brs.page_source
        analyze_zhihu(hcode, fzhihu)
    brs.close()


def name():
    return 'read.txt'
