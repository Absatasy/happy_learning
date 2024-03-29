# -*- coding:utf-8 -*-
"""
Author:  KleverX      智能、安全、高效、省心
Create:  2019.07.27 08:20
Edit:    2019.08.23 12:00
功能实现：每日全自动文章、视频、时长、分享等一套29分
"""


import os
import time
import math
import random
import subprocess
from time import sleep
from appium import webdriver


# 全局参数
p = 30  # p阅读文章分数，p+5视听，p+10文章时长，p+15视听时长，p+45收藏，p+50分享，p+55评论   【未实现 p+20每日答题，p+35挑战答题】
article_bar = ["人事", "国际", "法纪", "要闻", "新思想", "发布", "实践", "综合", '教育',
               "健康", "纪实", "时评", "思考", "旅游", '传播中国']
comments = ["好好学习，天天向上。", "学海无涯苦作舟", "这个你可以自己修改", "多加一点评论。"
            "大家的评论最好不要一样。", "要不然系统发现你经常评论一样的。", "自己用个记事本保存下来。"]
path = os.getcwd() + '/article_bar_index.txt'


def init_driver():
    desired_caps = {
        'platformName': 'Android',
        'platformVersion': '5.1.1',
        'deviceName': '127.0.0.1:62001',
        'appPackage': 'cn.xuexi.android',
        'appActivity': 'com.alibaba.android.rimet.biz.SplashActivity',
        'noSign': True,
        'noReset': True,
        'newCommandTimeout': 3600,
        "unicodeKeyboard": True,
        "resetKeyboard": True
    }
    return desired_caps


def devices_size():
    return driver.get_window_size()


def close_volume():
    print('关闭模拟器音量。')
    driver.press_keycode(164)   # 音量减小键25; 扬声器静音键 164.
    sleep(1)


def print_time(param):
    print(param, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


def creat_file(paths):
    if not os.path.exists(paths):
        with open(paths, 'w') as f:
            f.write('0')
            f.close()


def read_judge(paths):
    creat_file(paths)
    with open(paths, 'r') as f:
        t = f.readline()
        if t.isnumeric():
            if int(t) < len(article_bar):
                return int(t)
            else:
                return 0
        else:
            return 0


def write_files(paths, param):
    with open(paths, 'w') as f:
        f.write(param)
        f.close()


def enter_score_page():
    print('进入积分页面……')
    driver.find_element_by_accessibility_id("学习").click()
    sleep(1)
    driver.find_element_by_id("cn.xuexi.android:id/comm_head_xuexi_score").click()
    sleep(4)


def get_score(param):
    view_elements = driver.find_elements_by_class_name('android.view.View')
    ele_title = view_elements[param-2].text
    ele_score = view_elements[param].text
    lack_score = int(ele_score[9]) - int(ele_score[2])
    msg = ele_title + '分数还差' + str(lack_score)
    return msg


def get_click(param):
    ele_click = driver.find_elements_by_class_name('android.view.View')[param]
    ele_click.click()


def study_time(n, t):
    study_t = 0
    while study_t < t:
        sleep(6)
        scroll(0)
        sleep(7)
        study_t += 13
        print(f'{n}已学习{str(study_t)}秒;')


def scroll(param):
    size = devices_size()
    x = size['width']
    y = size['height']
    x1 = 4/5 * x
    y1 = 8/10 * y
    y2 = [6/10 * y, 1/10 * y]
    driver.swipe(x1, y1, x1, y2[param], 300)
    sleep(2)


def click_coordinates(param):
    size = devices_size()
    x = size['width']
    y = size['height']
    half_x = 4/5 * x
    click_list = [3/10 * y, 5/10 * y, 2/3 * y, 17/20 * y]
    print(f"点击第{str(param)}个点。")
    sleep(1)
    driver.tap([(half_x, click_list[param])], 110)
    sleep(2)


def cycle_click(pieces, n, t):
    for i in range(pieces):
        while i > 3:
            i = i - 4
            pieces = pieces - 4
        click_coordinates(i)
        study_time(n, t)
        driver.back()
        sleep(2)
        if i == 3:
            scroll(1)
    print(f'{n}学习结束')
    sleep(2)


def choose_channel():
    bar_index = read_judge(path)
    sleep(2)
    bar = article_bar[bar_index]
    driver.find_element_by_xpath("//android.widget.ImageView[@index=0][@instance=3]").click()
    print(f"进入{bar}频道")
    sleep(1)
    b = f'//android.widget.TextView[@text="{bar}"]'
    driver.find_element_by_xpath(b).click()
    bar_index = str(bar_index + 1)
    write_files(path, bar_index)
    sleep(2)


def article_read():
    msg = get_score(p)
    n = msg[:4]
    pieces = int(msg[-1])
    r_time = 12
    while pieces > 0:
        print(f'{n}还差{pieces}分。')
        get_click(p+1)
        sleep(2)
        choose_channel()
        cycle_click(pieces, n, r_time)
        print(f"{n}结束。")
        enter_score_page()
        pieces = int(get_score(p)[-1])
    print(f'2.{n}任务已完成！\n', "-" * 32)
    sleep(2)


def video_study():
    msg = get_score(p+5)
    n = msg[:4]
    pieces = int(msg[-1])
    v_time = 12
    size = devices_size()
    x1 = 97/100 * size['width']
    y = [2/5 * size['height'], 3/4 * size['height']]
    while pieces > 0:
        print(f'{n}还差{pieces}分。')
        get_click(p+6)
        driver.find_element_by_accessibility_id("百灵").click()
        sleep(1)
        for i in range(math.ceil(pieces/2)):
            driver.find_element_by_xpath('//android.widget.TextView[@text="炫"]').click()
            sleep(1)
            for j in range(2):
                driver.tap([(x1, y[j])], 110)
                study_time(n, v_time)
                driver.back()
                sleep(2)
        print(f"{n}结束。")
        enter_score_page()
        pieces = int(get_score(p+5)[-1])
    print(f'3.{n}任务已完成！\n', "-" * 32)
    sleep(2)


def read_time():
    msg = get_score(p+10)
    n = msg[:6]
    r_score = int(msg[-1])
    while r_score > 0:
        print(f'{n}还差{r_score}分,需要{r_score * 2 + 1}分钟。')
        scroll(0)
        get_click(p+11)
        sleep(2)
        rt = r_score * 2 * 60 + 66
        cycle_click(1, n, rt)
        print(f"{n}结束。")
        enter_score_page()
        r_score = int(get_score(p+10)[-1])
    print(f'4.{n}任务已完成！\n', "-" * 32)
    sleep(2)


def media_time():
    msg = get_score(p+15)
    n = msg[:6]
    m_score = int(msg[-1])
    while m_score > 0:
        print(f'{n}还差{m_score}分,需要{m_score * 3 + 1}分钟。')
        scroll(0)
        get_click(p+16)
        sleep(2)
        driver.find_element_by_xpath('//android.widget.TextView[@text="联播频道"]').click()
        sleep(2)
        mt = m_score * 3 * 60 + 66
        cycle_click(1, n, mt)
        print(f"{n}结束。")
        enter_score_page()
        m_score = int(get_score(p+15)[-1])
    print(f'5.{n}任务已完成！\n', "-" * 32)
    sleep(2)


def star_share_comment():
    star = int(get_score(p + 45)[-1])
    share = int(get_score(p + 50)[-1])
    comment = int(get_score(p + 55)[-1])
    max_score = max(star, share, comment)
    while max_score > 0:
        print("评论收藏分享来一套。")
        driver.back()
        sleep(2)
        driver.find_element_by_id("cn.xuexi.android:id/home_bottom_tab_icon_large").click()
        sleep(2)
        choose_channel()
        for l in range(2):
            click_coordinates(l)
            if comment > 0:
                driver.find_element_by_xpath('//android.widget.TextView[@text="欢迎发表你的观点"]').click()
                sleep(2)
                c = random.choice(comments)
                driver.find_element_by_xpath('//android.widget.EditText[@text="好观点将会被优先展示"]').send_keys(c)
                sleep(1)
                driver.find_element_by_xpath('//android.widget.TextView[@text="发布"]').click()
                sleep(2)
                driver.find_element_by_xpath('//android.widget.TextView[@text="删除"]').click()
                sleep(1)
                driver.find_element_by_id("android:id/button1").click()
                sleep(1)
            if star > 0:
                driver.find_element_by_xpath('//android.widget.ImageView[1][@index="2"]').click()
                sleep(1)
            if share > 0:
                driver.find_element_by_xpath('//android.widget.ImageView[2][@index="3"]').click()
                sleep(2)
                driver.find_element_by_xpath('//android.widget.ImageView[1]'
                                             '[@resource-id="cn.xuexi.android:id/img_gv_item"][@instance="0"]').click()
                sleep(2)
                driver.back()
                sleep(2)
            driver.back()
            sleep(2)
        print("收藏、评论、分享结束！")
        enter_score_page()
        star = int(get_score(p + 45)[-1])
        share = int(get_score(p + 50)[-1])
        comment = int(get_score(p + 55)[-1])
        max_score = max(star, share, comment)
    print('6.收藏、评论、分享任务已完成！\n', "-" * 32)
    sleep(2)


def happy_learning():
    enter_score_page()
    article_read()
    video_study()
    star_share_comment()
    read_time()
    media_time()
    print('今日所有自动学习任务已完成！')


def connect_devices():
    print('正在链接模拟器/设备……')
    os.system('adb.exe connect 127.0.0.1:62001')
    sleep(2)


if __name__ == '__main__':
    print_time("开始时间：")
    os.popen(r'E:\00Develop\Nox\bin\NoxConsole.exe launch -name:夜神模拟器')  # 1.更改为你电脑上夜神模拟器的位置
    print('正在打开夜神模拟器，请稍等……')
    sleep(21)
    print('正在打开appium……')
    subprocess.Popen('appium', shell=True)
    sleep(10)
    connect_devices()
    print('正在打开driver……')
    driver = webdriver.Remote('http://localhost:4723/wd/hub', init_driver())
    sleep(10)
    close_volume()
    happy_learning()
    print_time('结束时间：')
