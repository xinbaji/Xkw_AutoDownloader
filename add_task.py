import os
import json

task = []
count = 1

email = input("请输入接收者邮箱（无需发送请留空回车）：")
if "@" in email and "com" in email:
    email = email
else:
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
