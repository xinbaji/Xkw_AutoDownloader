import os
from utils.encrypt import pwdcfiiro1c,usnmdcfiiro1cqqt
from utils.selenium import Driver
from data.path import Xpath,Css
from config.config import Config
from time import sleep
import smtplib
from email import policy
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from utils.log import Log
import yagmail
import json
from utils.selenium import shutil
from utils.email import mail
class Xkw:
    def __init__(self) -> None:
        #初始化 检测config内的用于下载的账号密码，若没有要求用户手动输入。
        
        self.config=Config()
        
        #检测download文件夹
        if os.path.exists("./download") == False:
            os.makedirs("download")
            os.makedirs("tasks",exist_ok=True)
            
        self.isLogin = 0
        self.xpath=Xpath()
        self.css=Css()
        self.log=Log('main','i')
        self.mail=mail()
        
        
    def login(self):    
        
        self.driver.wait_to_be_visible(self.css.login_button()).click()
        self.driver.wait_to_be_visible(self.xpath.login_switch_button())
        sleep(5)
        self.driver.wait_to_be_visible(self.xpath.login_switch_button()).click()
        print(self.config.get_encryed_val(self.config.username()))
        print(self.config.get_encryed_val(self.config.password()))
        self.driver.wait_to_be_visible(self.xpath.login_username_input()).send_keys(self.config.username())
        self.driver.wait_to_be_visible(self.xpath.login_password_input()).send_keys(self.config.password())
        self.driver.wait_to_be_visible(self.xpath.login_commit_button()).click()
        self.driver.refresh()
        self.driver.driver.implicitly_wait(60)
        self.driver.save_cookies()
        self.config.save_to_config_file()
        
    def download(self,url):
        
        
        #检测是否登录
        self.driver.get(url,cookies=False)
        self.driver.driver.implicitly_wait(60)
        if self.isLogin == 0:
            self.login()
        self.driver.wait_to_be_visible(self.xpath.ppt_download_button())
        self.driver.force_click(self.xpath.ppt_download_button())
        self.isLogin = 1
        self.driver.switch_to_iframe(self.xpath.download_iframe())
        self.driver.wait_to_be_clickable(self.xpath.download_confirm_button())
        sleep(2)
        self.driver.wait_to_be_clickable(self.xpath.download_confirm_button()).click()
        self.driver.switch_to_default_frame()
        sleep(15)
        self.driver.get("https://www.zxxk.com/")
        
    
    def get_filelist(self):
        while True:
            count = 0
            filelist=os.listdir(".\download")
            if len(filelist) != 0:
                for i in range(0,len(filelist),1):
                    if 'cr' in filelist[i]:
                        self.log.info("下载未完成")
                        sleep(5)
                        break
                    else:
                        filelist[i]='.\\download\\'+filelist[i]
                        count += 1
                if count == len(filelist):
                    return filelist
                    
    def send_yagmail(self,recipientAddrs):
         
        yag_server= yagmail.SMTP(user=self.config.send_from_email(),password=self.config.code(),host='smtp.qq.com')
        email_to=[recipientAddrs,]
        email_attachment_list=self.get_filelist()
        email_title=email_attachment_list[0].replace('.\\download\\',"") + '等文件 (自动发送）'
        email_content='您的资料已发送，请查收哦~'
         
        yag_server.send(email_to,email_title,email_content,email_attachment_list)
        self.log.info("发送成功！")
        yag_server.close()
        
    def sendmail_attachments(self,recipientAddrs:str):
        email_attachment_list=os.listdir(".\download")
        file_path=".\\download\\"
        self.mail.sendmail(recipientAddrs=recipientAddrs,file_path=file_path,files_nameList=email_attachment_list)
    def update_status(self,status):
        with open("./tasks/status.json","w") as f:
                    json.dump(status,f)
                    f.close()     
    def get_task(self):
        self.log.info("开始检测任务队列")
        download_location=os.path.join(os.getcwd(),"download")
        prefs = {
                    "download.default_directory": download_location
                }
        self.driver=Driver(prefs)
        self.update_status("done")
        while True:
            if os.path.exists("./tasks/task.json") == True:
                with open("./tasks/task.json","r") as f:
                    task=json.load(f)
                    f.close()  
                os.remove("./tasks/task.json")
                self.update_status("busy")
                
                
                for i in task['task']:
                    self.download(i)
                filelist=self.get_filelist()
                if task['recv_email'] != "":
                    self.sendmail_attachments(task['recv_email'])
                self.log.info("下载发送任务结束，准备接受新任务")
                with open("./tasks/status.json","r") as f:
                    status=json.load(f)
                    f.close()
                shutil.rmtree("./download")
                os.makedirs("download")
                self.update_status("done")
            else:
                sleep(5)
                    
#Xkw().get_task()
Xkw().sendmail_attachments("407510271@qq.com")
        
        
                
                
                
                