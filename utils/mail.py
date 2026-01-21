import yagmail
from smtplib import SMTPSenderRefused, SMTPException
import os
from utils.log import Log

def SMTPErrorHandler(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except SMTPSenderRefused as sr:
            self.log.error("Message too large.")
        except SMTPException as se:
            self.log.error(f"SMTP error occurred: {str(se)}")
        except Exception as e:
            self.log.error(f"Unexpected error during email sending: {str(e)}")
    
    return wrapper

class Mail(object):
    def __init__(self) -> None:
        self.senderAddrs = ""
        self.passcode = ""
        self.sendFileLocation = ".\\temp"
        
        self.host_domain = self.get_host_domain()
        self.log = Log("mail", "d").logger
        self.attachments = self.get_attachment_list()
        self.title = self.get_email_title()
        self.content = self.get_email_content()

    def get_email_title(self):
        if self.attachments:
            return self.attachments[0].replace(".\\temp\\", "") + "等文件 (自动发送）"
        else:
            return "文件附件 (自动发送）"

    def get_host_domain(self):
        host_domain_list = ["163.com", "qq.com"]
        if not self.senderAddrs:
            return None
        for i in host_domain_list:
            if i in self.senderAddrs:
                host_domain = "smtp." + i
                return host_domain
        return None

    def get_attachment_list(self):
        temp_dir = ".\\temp"
        if os.path.exists(temp_dir) and os.path.isdir(temp_dir):
            for i in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, i)
                if os.path.isfile(file_path): 
                    self.email_attachment_list.append(file_path)
        return self.email_attachment_list

    def get_email_content(self):
        return "您的资料已发送，请查收哦~"

    @SMTPErrorHandler
    def send(self, recipientAddrs: list):
        
        if not self.senderAddrs or not self.passcode:
            self.log.error("Sender address or passcode not configured.")
            return
            
        if not self.host_domain:
            self.log.error("Host domain not configured properly.")
            return

        yag_server = None
        
        yag_server = yagmail.SMTP(
            user=self.senderAddrs,
            password=self.passcode,
            host=self.host_domain,
        )

        for i in recipientAddrs:
            self.log.info("正在发送邮件至：" + i)
            yag_server.send(i, self.title, self.content, self.attachments) 
            self.log.info("发送成功！")
    
        if yag_server:
            yag_server.close()