# -*- coding:utf-8 -*-
import itchat
import os, json, time, requests, traceback
from Fortunes import get_fortune, get_emoji
from loadUsers import get_users


# Hyper parameters

weather_url = "http://api.avatardata.cn/Weather/Query?key="
weather_key = "ad0400dae57c42bbac78b8e2352e362e"
hist_url = "http://api.avatardata.cn/HistoryToday/LookUp?key="
hist_key = "bf7a5437f9254520bab5eaf44d122f1d"


# User list : [name / position / individual / sex(M/W/G)]
users = [
    ["品味之家", "宁波", False, 'G'], 
    ["两对", "宁波", False, 'G'],
    ["Pepper*79", "成都", True, 'W'],
    ["尼玛来啦~", "长沙", True, 'W'],  # ["稷下歌吟", "长沙", True, 'W'],
]

# Msg buffers : [Morning, position, greet]
buffer = []  # 早上和傍晚的缓冲


# Helpers

def trans_weather_like_man(dawn, day, night):
    """如同天气预报"""
    if dawn == day == night:
        return "全天%s" % dawn
    elif dawn == day:
        return "白天%s，夜里转%s" % (dawn, night)
    elif day == night:
        return "早上%s，午后转%s" % (dawn, day)
    else:
        return "白天%s转%s，晚间%s" % (dawn, day, night)


def morning_nightfall_msg(position, morning):
    """用于早晨和傍晚"""
    if len(buffer) != 0 and buffer[0] == morning and buffer[1] == position:
        return buffer[2]
    buffer.clear()

    url = weather_url + weather_key + "&cityname=" + position

    data = json.loads(requests.get(url).text, encoding='utf-8')
    if data['error_code'] != 0:
        print("Error code : ", data['error_code'])
        return ""

    # Data
    result = data['result']
    life_info = result['life']['info']
    pm25 = result['pm25']['pm25']
    day_weather = result['weather'][0]['info']
    weather = trans_weather_like_man(
        day_weather['dawn'][1], day_weather['day'][1], day_weather['night'][1]
    )

    # 空气质量
    quality = "空气质量为%s, %s。\n" % (pm25['quality'], pm25['des'])

    # 晚上信息
    if not morning:
        realtime_t = result['realtime']['weather']['temperature']
        greet = "Good evening~~\n%s实时气温%s℃，%s——From CloudBot%s" % (position, realtime_t, quality, get_emoji())
        buffer.append(not morning)
        buffer.append(position)
        buffer.append(greet)

        return greet

    # 基本天气状况
    life_reminder = "今天最低气温%s℃，最高气温%s℃。\n%s。天气%s，%s\n" % (
                    day_weather['dawn'][2], day_weather['day'][2],
                    weather,
                    life_info['chuanyi'][0], life_info['chuanyi'][1]
    )

    greet = "Morning~~\n" + position + life_reminder + quality + "——From CloudBot" + get_emoji()
    buffer.append(morning)
    buffer.append(position)
    buffer.append(greet)

    return greet


def night_msg(fortune=True, row=5):
    """用于夜间"""
    if fortune:
        return "Good night~~\n" + get_fortune() + "——From CloudBot" + get_emoji()
    else:
        cur_date = (time.localtime().tm_mon, time.localtime().tm_mday)
        url = hist_url + hist_key + "&yue=%d&ri=%d&type=1&rows=%d" % (cur_date[0], cur_date[1], row)
        hist_data = json.loads(requests.get(url).text)['result']

        hists = "历史上的今天：\n"
        for hist in hist_data:
            hists += "%s年 %s\n" % (hist['year'], hist['title'])

        return "Good night~~\n" + hists + "——From CloudBot" + get_emoji()


# Tasks
def morning_evening_task(position, username, individual, morning):
    msg = morning_nightfall_msg(position=position, morning=morning)
    try:
        if individual:
            user = itchat.search_friends(name=username)[0]
            user.send(msg)
        else:
            user = itchat.search_chatrooms(name=username)[0]
            user.send(msg)
    except Exception as morning_err:
        itchat.send("%s cannot receive msg! And error is %s" % (username, str(morning_err)), toUserName='filehelper')
        itchat.send(msg, toUserName='filehelper')


def night_task(username, individual):
    msg = night_msg()
    try:
        if individual:
            user = itchat.search_friends(name=username)[0]
            user.send(msg)
        else:
            user = itchat.search_chatrooms(name=username)[0]
            user.send(msg)
    except Exception as night_err:
        itchat.send("%s cannot receive msg! And error is %s" % (username, str(night_err)), toUserName='filehelper')
        itchat.send(msg, toUserName='filehelper')


# Heartbeat

def heartbeat():
    now = time.localtime()
    itchat.send(
        "%d:%d:%d HeartBeat\n%s" % (now.tm_hour, now.tm_min, now.tm_sec, get_fortune()),
        toUserName='filehelper')


# Timer

def timer():
    global users  # If not global, can cause rename.
    users = get_users()

    """Infinite loops"""
    while True:
        now = time.localtime()

        # Morning
        if now.tm_hour == 7 and now.tm_min == 0:
            for i in range(len(users)):
                morning_evening_task(position=users[i][1], username=users[i][0], individual=users[i][2], morning=True)
                time.sleep(0.1)

            print("%2d:%2d" % (now.tm_hour, now.tm_min), "Morning task finished")

        # Load users
        elif now.tm_hour == 12 and now.tm_min == 0:
            users = get_users()

        # Evening
        elif now.tm_hour == 19 and now.tm_min == 0:
            for i in range(len(users)):
                morning_evening_task(position=users[i][1], username=users[i][0], individual=users[i][2], morning=False)
                time.sleep(0.1)

            print("%2d:%2d" % (now.tm_hour, now.tm_min), "Evening task finished")

        '''
        # Night
        elif now.tm_hour == 22 and now.tm_min == 0:
            for i in range(len(users)):
                night_task(username=users[i][0], individual=users[i][2])
                time.sleep(0.1)

            print("%d:%d:%d" % (now.tm_hour, now.tm_min, now.tm_sec), "Night task finished")
        '''
        
        # Heartbeat
        if now.tm_min % 15 == 0:
            heartbeat()

        # Regulation
        time.sleep(61 - time.localtime().tm_sec)


if __name__ == '__main__':
    try:
        if os.path.exists('./itchat.pkl'):
            os.remove('./itchat.pkl')
        itchat.auto_login(hotReload=True, enableCmdQR=2)
        itchat.send('Hello!', toUserName='filehelper')
        timer()
    except Exception as errs:
        itchat.send(msg=str(errs), toUserName='filehelper')
    except:
        with open("LastError.txt", "w") as f:
            traceback.print_exc(file=f)
