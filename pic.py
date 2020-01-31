import os
import re
import tkinter.filedialog
from tkinter import *

import PIL.Image as image
import jieba
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import wordcloud

import pa

filename = ''
picture = ''
page = ''
wordmax = 200
stops = ['年月日', '天前']
word = ''
search = ''
searchlist = ["百度", "必应", "谷歌", "知乎", "微信（需要扫码登录）", "微博（需要扫码登录）"]
fuxuanint = [0, 0, 0, 0, 0, 0]
ch = [0, 0, 0, 0, 0, 0]
result_path = ''


def insert_text(text,  imname, position):
    fone_type_file="C:\\Windows\\Fonts\\msyhbd.ttc"
    font_size=50
    im = Image.open(imname)
    datas = text.split('\n')
    data = ''
    if not datas:
        datas = [text]
    for d in datas:
        if not d:
            d = ' '
        elif len(d) > 31:
            d1 = d[:30] + '\n'
            d2 = d[30:]
            d = d1 + ' \n'+ d2
        data += (d +'\n')
        data += ' \n'
    data = data[:-1]
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype(fone_type_file, font_size)

    dr.text(position, data, font=font, fill="#EE3D11", spacing=0, align='left')
    im.save(imname)
    return im, len(datas)


# 图片拼接
def image_compose():
    column = 0
    l = []
    for i in range(len(fuxuanint)):
        if fuxuanint[i].get() == 1:
            column += 1
            l.append(i)
    size = 2048
    size1 = size // 3 * 5
    to_image = image.new('RGB', (1 * size1, column * size))

    for x in range(column):
        from_image = image.open("result_" + searchlist[l[x]] + ".jpg").resize((size1, size), image.ANTIALIAS)

        to_image.paste(from_image, (0, x * size))
    return to_image.save('compose.jpg')


def run1():
    def xzpic():
        global picture
        picture = tkinter.filedialog.askopenfilename()
        rd4.insert(index=0, string=picture)

    def xzpath():
        global result_path
        result_path = tkinter.filedialog.askdirectory()
        rd8.insert(0, result_path)

    def doit():
        global result_path
        if result_path != '':
            os.chdir(result_path)

        global wordmax, stops, page, filename, word, search
        word = lbword.get()
        page = rd7.get()
        wordmax = eval(rd5.get())
        ss = rd6.get()
        for ch in ',，':
            ss = ss.replace(ch, ' ')
        stops = ss.split()
        search = var.get()
        for i in range(len(fuxuanint)):
            if fuxuanint[i].get() == 1:
                filename = pa.name()
                if i == 0:
                    pa.pa_baidu(word, page)
                elif i == 1:
                    pa.pa_bing(word, page)
                elif i == 2:
                    pa.pa_google(word, page)
                elif i == 3:
                    pa.pa_zhihu(word, page)
                elif i == 4:
                    pa.pa_weixin(word, page)
                else:
                    pa.pa_weibo(word, page)

                ciyun(filename, picture, wordmax, stops, "result_" + searchlist[i] + ".jpg")
                insert_text(searchlist[i] + "生成: " + word, "result_" + searchlist[i] + ".jpg", (100, 100))
        image_compose()

    mod1 = Toplevel(root)
    mod1.title("网络爬虫")
    mod1.geometry('320x560')
    lb = Label(mod1, text="请选择搜索引擎")
    lb.pack()
    # var=StringVar()
    # comb=Combobox(mod1,textvariable=var,values=searchlist)
    # comb.pack()
    for i in range(len(fuxuanint)):
        fuxuanint[i] = IntVar()
        ch[i] = Checkbutton(mod1, text=searchlist[i], variable=fuxuanint[i], onvalue=1, offvalue=0)
        ch[i].pack()
    lb2 = Label(mod1, text="请输入要搜索的词")
    lb2.pack()
    lbword = Entry(mod1)
    lbword.pack()
    lb4 = Label(mod1, text="请选择图片")
    lb4.pack()

    rd4 = Entry(mod1)
    rd4.pack()
    lbn4 = Button(mod1, text="选择", command=xzpic)
    lbn4.pack()

    lb5 = Label(mod1, text="请输入最多生成词的个数：")
    lb5.pack()

    rd5 = Entry(mod1)
    rd5.pack()

    lb6 = Label(mod1, text="请输入跳过的词，用逗号或空格隔开：")
    lb6.pack()

    rd6 = Entry(mod1)
    rd6.pack()

    lb7 = Label(mod1, text="请输入要爬虫的页数")
    lb7.pack()

    rd7 = Entry(mod1)
    rd7.pack()

    lb8 = Label(mod1, text='请选择图片保存目录：')
    lb8.pack()

    rd8 = Entry(mod1)
    rd8.pack()
    lbn6 = Button(mod1, text='选择路径', command=xzpath)
    lbn6.pack()

    lbn5 = Button(mod1, text="生成", command=doit)
    lbn5.pack()

    return


def run2():
    def xzart():
        global filename
        filename = tkinter.filedialog.askopenfilename()
        rd3.insert(index=0, string=filename)

    def xzpic():
        global picture
        picture = tkinter.filedialog.askopenfilename()
        rd4.insert(index=0, string=picture)

    def xzpath():
        global result_path
        result_path = tkinter.filedialog.askdirectory()
        rd8.insert(0, result_path)

    def doit():
        if result_path != '':
            os.chdir(result_path)
        global wordmax, stops
        wordmax = eval(rd5.get())
        ss = rd6.get()
        for ch in ',，':
            ss = ss.replace(ch, ' ')
        stops = ss.split()

        ciyun(filename, picture, wordmax, stops, "result" + ".jpg")

    mod2 = Toplevel(root)
    mod2.title("文章生成")
    mod2.geometry('320x420')
    lb3 = Label(mod2, text='请选择文章：')
    lb3.pack()

    rd3 = Entry(mod2)
    rd3.pack()
    lbn3 = Button(mod2, text="选择", command=xzart)
    lbn3.pack()

    lb4 = Label(mod2, text="请选择图片")
    lb4.pack()

    rd4 = Entry(mod2)
    rd4.pack()
    lbn4 = Button(mod2, text="选择", command=xzpic)
    lbn4.pack()

    lb5 = Label(mod2, text="请输入最多生成词的个数：")
    lb5.pack()

    rd5 = Entry(mod2)
    rd5.pack()

    lb6 = Label(mod2, text="请输入跳过的词，用逗号或空格隔开：")
    lb6.pack()

    rd6 = Entry(mod2)
    rd6.pack()

    lb8 = Label(mod2, text='请选择图片保存目录：')
    lb8.pack()

    rd8 = Entry(mod2)
    rd8.pack()
    lbn6 = Button(mod2, text='选择路径', command=xzpath)
    lbn6.pack()

    lbn5 = Button(mod2, text="生成", command=doit)
    lbn5.pack()
    return


def ciyun(article, picture, word_max, stopwords, result_path1):
    with open(article, 'r', encoding='utf-8') as f:
        word = f.read()
        f.close()
    # for i in range(len(word)):
    #     word[i] = word[i].replace(' ','')
    stopwords.append('年月日')
    stopwords.append('一个')
    stopwords.append('天前')
    stopwords.append('很多')
    word = word.replace(' ', '')
    image1 = np.array(image.open(picture))
    font = "C:\\Windows\\Fonts\\msyhbd.ttc"
    resultword = re.sub("[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\。\@\#\\\&\*\%]", "", word)
    wordlist_after_jieba = jieba.cut(resultword)
    wl_space_split = " ".join(wordlist_after_jieba)
    ls = stopwords
    sw = set(stopwords)
    for i in range(len(ls)):
        sw.add(ls[i])

    my = wordcloud.WordCloud(
        scale=4,
        font_path=font,
        mask=image1,
        stopwords=sw,
        background_color='white',
        max_words=word_max,
        max_font_size=60,
        random_state=20
    ).generate(wl_space_split)

    plt.imshow(my)
    plt.axis("off")
    plt.show()

    my.to_file(result_path1)
    return


root = Tk()
root.geometry('460x240')
root.title("模式选择")

lb1 = Label(root, text="欢迎使用本工具，请选择一种方式生成词云：")

lb1.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.1)

var = IntVar()
rd1 = Radiobutton(root, text="关键词爬虫生成", variable=var, value=0, command=run1)
rd1.place(relx=0.1, rely=0.4, relwidth=0.3, relheight=0.1)

rd2 = Radiobutton(root, text="本地文章生成", variable=var, value=1, command=run2)
rd2.place(relx=0.6, rely=0.4, relwidth=0.3, relheight=0.1)

root.mainloop()
