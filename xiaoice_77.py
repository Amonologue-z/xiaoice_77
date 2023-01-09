import threading
import time
import websocket
import configparser
import json
import configparser
import requests
import hashlib
import sys
import re
import datetime
from html import unescape
config = configparser.ConfigParser()
config.read("config.ini", encoding="utf-8")
HOST = 'https://fishpi.cn'
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
API_KEY=''
string_woshou = ''
string_login = ''

def html_to_plain_text(html):
    
    text = re.sub('<head.*?>.*?</head>', '', html, flags=re.M | re.S | re.I)
    text = re.sub('<a\s.*?>', '', text, flags=re.M | re.S | re.I)
    text = re.sub('<.*?>', '', text, flags=re.M | re.S)
    text = re.sub(r'(\s*\n)+', '\n', text, flags=re.M | re.S)
    text = text.replace('状态：','\n\n状态')
    text = text.replace('点击查看版本更新说明点击查看游戏开发计划','')
    text = text.replace('人物等级：','\n人物等级：')
    text = text.replace('当前经验：','\n当前经验：')
    text = text.replace('升级经验：','\n升级经验：')
    text = text.replace('斗气属性：','\n斗气属性：')
    text = text.replace('血脉等级：','\n血脉等级：')
    text = text.replace('功法等级：','\n功法等级：')
    text = text.replace('血量：','\n血量：')
    text = text.replace('攻击：','\n攻击：')
    text = text.replace('防御：','\n防御：')
    text = text.replace('道侣：','\n道侣：')
    text = text.replace('宗门：','\n宗门：')
    text = text.replace('大地图：','\n大地图：')
    text = text.replace('互动：','\n\n互动：')
    text = text.replace('吐纳次数：','\n吐纳次数：')
    text = text.replace('历练次数：','\n历练次数：')
    text = text.replace('嗑药次数：','\n嗑药次数：')
    text = text.replace('背包：','\n\n背包：')
    text = text.replace('[金币]：','\n[金币]：')
    text = text.replace('[丹药]：','\n[丹药]：')
    text = text.replace('[材料]：','\n[材料]：')
    text = text.replace('[武器]：','\n[武器]：')
    text = text.replace('[防具]：','\n[防具]：')
    text = text.replace('[异火]：','\n[异火]：')
    text = text.replace('装备：','\n\n装备：')
    return unescape(text)
def read_config_and_login():
    global API_KEY
    try:
        config = configparser.ConfigParser()
        config.read("config.ini", encoding="utf-8")
        username = config.get('login', 'username')
        password = config.get('login','password')
        erbu_code = str(config.get('login','2FA'))
    except:
        print("请检查配置文件是否合法")
        sys.exit(1)
    code = ''
    if erbu_code == '1':   #开启二步验证
        code = str(input('请输入二步验证码'))
        params = {'nameOrEmail': username,'userPassword':hashlib.md5(str(password).encode('utf-8')).hexdigest(),'mfaCode':code}
        resp = requests.post(HOST + "/api/getKey",json=params,headers={'User-Agent': UA})
        body = json.loads(resp.text)
    
    if erbu_code == '0':   #不开启二步验证
        code = ''
        params = {'nameOrEmail': username,'userPassword':hashlib.md5(str(password).encode('utf-8')).hexdigest(),'mfaCode':code}
        resp = requests.post(HOST + "/api/getKey",json=params,headers={'User-Agent': UA})
        body = json.loads(resp.text)

        
    if body['code'] == 0:
        
        print('登陆成功'+username+ '   欢迎使用 由七七开发的命令行版小冰游戏~')
        print('现在时间是：'+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        print('祝你摸鱼愉快~~~')
        print("更多功能与趣味游戏请访问网页端: " + HOST)
        API_KEY = body['Key']
        print(config.get("login","apikey"))
        if config.get("login","apikey") == '':
            config.set('login','apikey',API_KEY)
            print("已经写入配置文件")
            #print(config.get('login','apikey'))
            with open("config.ini","w+") as f:
                config.write(f)
            
        return True
    elif body['code'] == -1 and body['msg'] == '两步验证失败，请填写正确的一次性密码':
        print("两步验证失败, 请修改配置文件")
        
    else:
        print("登陆失败: " + body['msg'])
        sys.exit(1)
def get_uid_and_set_str():
    global string_woshou
    global string_login
    url = HOST+"/user/"+config.get('login', 'username')

    headers = {
       'User_Agent':UA
    }
    response = requests.get(url)
    body_2 = json.loads(response.text)
    uid = int(body_2['oId'])

    string_woshou = {
        'type' : 'setUser',
        'user' : str(config.get('login','username')),
        'ck' : 'null',
        'uid' : uid
        }
    string_login = {
        'type': 'login',
        'ck': 'null',
        'msg':'登录 '+ str(config.get('xiaoice','xiaoice_password'))
        
        }
def renderMsg(msg):
    if msg['type'] == 'setCK':
        obj = open('.\config.json','w')
        obj.write(str(msg['ck']))
        obj.close
        obj = open('.\config.json','w')
        obj.write(str(msg['ck']))
        print(msg['msg'])
        obj.close
    if msg['type'] == 'gameMsg':
        print(html_to_plain_text(msg['msg'])+'\n')
        if msg['user'] == 'all':
            print('【全服公告】' + msg['msg'])
        


def when_message(ws, message):
    json_body = json.loads(message)
    renderMsg(json_body)
 
 
# 当建立连接后，死循环不断输入消息发送给服务器
# 这里需要另起一个线程
def when_open(ws):

    def run():
        def read_ck():
            with open('config.json','r') as fp:          
                data = fp.readlines()
                return data[0]
            return response
        def send_msg(msg):
            a = json.dumps(msg)
            ws.send(a)

            time.sleep(0.5)
        def woshou():
            a = json.dumps(string_woshou)
            ws.send(a)
            time.sleep(0.5)
            
        def login():
            global latest_message
            a = json.dumps(string_login)
            ws.send(a)

       

        woshou()
        login()
        time.sleep(2)
        cookie = read_ck()

        while True:
            aaa = input(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+'  >')
            if aaa == 'Amonologue-七七':
                print("叮！恭喜你发现了个彩蛋，嘻嘻\n")
                print('https://file.fishpi.cn/2023/01/image-8e5e7338.png')
            string_user = {
            'type':'gameMsg',
            'ck':cookie,
            'msg':str(aaa)
            }
            send_msg(string_user)
    t = threading.Thread(target=run)
    # t.setDaemon(True)
    t.start()
 
def when_close(ws):
    print('连接关闭')
 
if __name__ == '__main__':
        if config.get('login','apikey') == '':
            read_config_and_login()
            print("登录成功，请重启软件")
        else:
            get_uid_and_set_str()
            print('欢迎使用 由七七开发的命令行版小冰游戏~')
            print('现在时间是：'+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            print('祝你摸鱼愉快~~~')
            ws = websocket.WebSocketApp('ws://game.yuis.cc/wss', on_message=when_message, on_open=when_open, on_close=when_close)
            ws.run_forever()
