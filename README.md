# Xkw_AutoDownloader
学科网资料全自动下载！！并且可以发送至邮箱！！
食用方法：1.安装所需要的库：(1)pip install selenium
                          (2)pip install yagmail
        1.5:先运行config中的config.py输入发送邮箱、授权码、学科网的用户名和密码
         2.运行main.py后台挂着
         3.运行add_task.py输入课件下载地址和发送邮箱。
         4.需要添加任务直接运行add_task.py添加任务，无需关闭main.py
         enjoy！

注意的点：1.由于qq邮箱的发送限制，邮箱只能发送50m以下的课件，目前想不到有啥好办法。
        2.使用过程中可能出现微信扫码和输入验证码，需要自己手动弄一下。
        3.测试下来同一ip或账号高频下载后，学科网会限速至几十kb每秒，不知道咋搞。
         
