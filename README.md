# Xkw_AutoDownloader

学科网资料全自动下载工具，支持自动登录、下载课件！

## 📖 项目简介

**Xkw_AutoDownloader** 是一款自动化下载学科网课件的工具，主要功能包括：

- ✅ 自动登录学科网账号
- ✅ 自动化下载课件资源
- ✅ 支持邮件发送下载的文件

---

## 🛠️ 安装依赖

> ⚠️ 请确保已安装 Python 3.x 及相关依赖包

```
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple
```


---

## 🚀 使用方法

### 1. 配置 `settings.py`

在 `settings.py` 文件中配置相关信息：

#### Setting:
```
username = "your_phone_number"  # 登录学科网的手机号
password = "your_password"      # 登录学科网的密码
download_location = ""          # 下载文件保存位置，为空则默认保存到./download目录
    
sender_email = ""               # 发送邮件的邮箱地址
sender_passcode = ""            # 邮箱授权码（不是登录密码）
send_files_location = ""        # 要发送的文件保存位置

```

配置项说明：

username: 学科网登录账号（通常是手机号）

password: 学科网登录密码

download_location: 下载文件的保存路径，留空则默认保存到项目根目录下的 download 文件夹

sender_email: 用于发送邮件的邮箱地址（QQ邮箱或163邮箱）

sender_passcode: 邮箱的授权码（不是邮箱登录密码），获取方式：在邮箱中申请开启SMTP服务时 邮箱给你提供的授权码

send_files_location: 邮件发送的文件路径

在 `settings.py` 文件中配置好相关参数后，运行 `main.py` 文件即可开始下载。

### 2. 编写主程序 `main.py` 并运行
- main.py` - 程序入口文件有范例，想下载几个课件就复制download函数几次 里面填上链接


### 主要模块说明

- `main.py` - 程序入口
  - 程序主入口，初始化下载器并执行下载任务：



- `setting.py` - 配置文件
  - 存储项目运行所需的各种配置参数。

- `downloader.py` - 下载核心模块
  - 包含下载功能的主要实现逻辑：

```
主要函数：
init(): 初始化下载器，设置下载路径、日志和浏览器驱动
handle_login_button(): 处理登录按钮点击，执行登录流程
handle_already_login(): 处理已登录状态
login(): 登录控制，判断是否需要登录
handle_download_iframe(): 处理下载iframe窗口
handle_no_iframe(): 处理无iframe情况
download(url: str) -> bool: 执行下载的核心函数，接受URL参数并返回下载状态

```

- `utils/controller.py` - 浏览器控制器
  - 封装了与浏览器交互的各种操作：

```
元素查找与等待
点击、输入等交互操作
页面导航与状态检查
截图功能
窗口切换等
```

- `utils/path.py` - 页面路径配置
  - 集中管理学科网页面元素的定位策略和表达式，包含：

```
登录按钮
用户名密码输入框
下载按钮
iframe元素
状态提示元素等

```

- `utils/mail.py` - 邮件发送功能
  - 提供邮件发送功能，支持发送下载的文件。

### Downloader函数详细用法

```

handle_download_iframe()
处理下载iframe窗口：

切换到iframe
点击确认下载按钮
切回主框架

handle_no_iframe()
处理不需要iframe的情况，通常为空实现。

download(url: str) -> bool
核心下载函数，接收URL参数：

访问指定链接
执行登录流程
点击下载按钮
处理下载过程中的各种情况
返回下载状态
```

### 注意事项

- 首次运行: 第一次运行时需要在settings.py配置发送邮箱、授权码、学科网的用户名和密码
- 下载链接: 仅支持课件的资料链接，如：https://www.zxxk.com/soft/39457903.html
- 权限限制: 根据学科网的等级（普通用户、网校通会员等），只能下载对应等级免费的课件资源，付费资源无法下载
- 手动操作: 使用过程中可能出现微信扫码和输入验证码，需要手动处理
- 频率限制: 同一IP或账号高频下载后，学科网会限速

---

### 常见问题


- Q: 邮箱发送有限制吗？ A: 由于各大邮箱的SMTP发送限制，邮箱只能发送50M以下的课件。

- Q: 下载速度很慢怎么办？ A: 可能是学科网对相同IP或账号的访问频率限制导致的，建议降低下载频率。

- Q: 出现验证码或微信验证怎么办？ A: 需要手动完成验证，程序会在这些步骤暂停等待用户操作。



---

### 许可证

```

声明：仅供学习交流使用，不得用于违法侵权途径。

如遇BUG，请提供log文件并提issue。
