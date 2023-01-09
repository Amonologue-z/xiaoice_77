# 前言

欢迎您使用七七开发的命令行版 小冰游戏~~~  如果觉得好用,给个star吧  (doge

本人的python学的不太好，代码或许也有许多bug，也并不简洁，您可以通过摸鱼派的方式联系我并可以在issue里面反馈bug以及建议，谢谢！:blush:

# 配置

:warning:注意，第一次使用的时候需要设置 config.ini  :warning:   config.json  请不要动

:warning:第一次登录如果有闪退的现象那么就重启一下软件

## config.ini 配置详解

| 字段             | 必要性 | 解释                                                |
| ---------------- | ------ | --------------------------------------------------- |
| username         | 必填   | 摸鱼派用户名 如: Amonologue                         |
| password         | 必填   | 摸鱼派密码  如:123456                               |
| 2fa              | 必填   | 摸鱼派是否开启二步验证  1为开启，0为关闭            |
| apikey           | 选填   | 摸鱼派apikey   自己会填的填一下，不会填可以自动登录 |
| xiaoice_password | 必填   | 摸鱼派小冰游戏密码  如: 123456                      |

# 使用方法

clone本项目把config.ini和config.json放在同一目录 

执行pip install 下载项目依赖

```cmd
pip install -r requirements.txt
```

执行python文件

```
python xiaoice_77.py
```

或者直接下载release的exe，与配置文件放在同一目录直接执行

# 鸣谢

登录模块部分参考 [摸鱼派聊天室Python客户端 (github.com)](https://fishpi.cn/forward?goto=https%3A%2F%2Fgithub.com%2Fgakkiyomi%2Fpwl-chat-python)
