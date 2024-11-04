import os
import json

task = []
count = 1
debug_mode = False  # 调试模式
if debug_mode == True:
    email = ""
    task = []
else:
    while True:
        email = input("请输入接收者邮箱（无需发送请留空回车）：")
        if "@" in email and "com" in email:
            break
        else:
            print("输入邮箱地址非法，请重新输入\n")
            email = ""

    while True:
        url = input("请输入想下载的第 " + str(count) + " 课件地址（输入#结束）：")

        if "zxxk.com/soft/" in url:
            task.append(url)
            count += 1
        elif url == "#":
            break
        else:
            pass


dic = {"recv_email": email, "task": task}
os.makedirs("tasks", exist_ok=True)
with open("./tasks/task.json", "w") as f:

    json.dump(dic, f)
    f.close()

print("任务生成成功！")
