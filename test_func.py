# -*- coding:utf-8 -*-
import os
import json
import time
import requests
import itchat
import traceback
from Fortunes import get_fortune, get_emoji
import loadUsers


# Hyper parameters

weather_url = "http://api.avatardata.cn/Weather/Query?key="
weather_key = "ad0400dae57c42bbac78b8e2352e362e"
hist_url = "http://api.avatardata.cn/HistoryToday/LookUp?key="
hist_key = "bf7a5437f9254520bab5eaf44d122f1d"


# User list : [name / position / individual / sex(M/W/G)]
users = [
    ["品味之家", "宁波", False, 'G'], ["两对", "宁波", False, 'G'], ["Pepper", "成都", True, 'W'], ["张启帆", "绍兴", True, 'M'],
    ["{ Aeonni }", "杭州", True, 'M'], ["尼玛来啦~", "长沙", True, 'W'], ["EWING", "长沙", True, 'M'], ["LIu_x1nGt0Ng", "长沙", True, 'W'],
    ["棖", "长沙", True, 'W'], ["乔越", "长沙", True, 'W'], ["薪dada", "长沙", True, 'W'], ["划啊划~", "长沙", True, 'W'],
    ["陶印荣", "长沙", True, 'M'], ["今天有雨", "长沙", True, 'W'], ["稷下歌吟", "长沙", True, 'M']
]


# Msg buffers : [Morning, position, greet]
buffer = [] # 早上和傍晚的缓冲


# Helpers

def trans_weather_like_man(dawn, day, night):
    return ""


def greeting_morning_nightfall(position, morning):
    return ""


def greeting_night(fortune=True, row=5):
    return ""


# Tasks

def morning_evening_task(position, username, individual, morning):
    try:
        if individual:
            user = itchat.search_friends(name=username)[0]
        else:
            user = itchat.search_chatrooms(name=username)[0]
    except Exception as morning_err:
        print(username, morning_err)


def night_task(username, individual):
    try:
        if individual:
            user = itchat.search_friends(name=username)[0]
        else:
            user = itchat.search_chatrooms(name=username)[0]
    except Exception as night_err:
        print(username, night_err)


# Heartbeat

def heartbeat():
    return


# Timer

def timer():
    global users

    print("Debugging")
    """Infinite loops"""
    while True:
        now = time.localtime()
        # Morning
        if now.tm_sec == 0:
            for i in range(len(users)):
                morning_evening_task(position=users[i][1], username=users[i][0], individual=users[i][2], morning=True)

            print("%2d:%2d" % (now.tm_hour, now.tm_min), "Morning task finished")

        # Load users
        elif now.tm_sec == 15:
            users = loadUsers.get_users()

        # Evening
        elif now.tm_sec == 30:
            for i in range(len(users)):
                morning_evening_task(position=users[i][1], username=users[i][0], individual=users[i][2], morning=False)

            print("%2d:%2d" % (now.tm_hour, now.tm_min), "Evening task finished")

        # Night
        elif now.tm_sec == 45:
            for i in range(len(users)):
                night_task(username=users[i][0], individual=users[i][2])

            print("%d:%d:%d" % (now.tm_hour, now.tm_min, now.tm_sec), "Night task finished")

        # Regulation
        time.sleep(2)


if __name__ == '__main__':
    try:
        itchat.auto_login(hotReload=True, enableCmdQR=2)
        itchat.send('Debugging', toUserName='filehelper')
        itchat.send_image(fileDir='2018.jpg', toUserName='filehelper')
        # timer()

    except:
        traceback.print_exc()
