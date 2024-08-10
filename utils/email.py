import smtplib
import logging
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.config import Config
from utils.log import Log

from email import encoders

class mail:
    def __init__(self) -> None:
        self.config=Config()
        self.from_addr=self.config.send_from_email()
        self.From = self.from_addr
        self.sercetcode = self.config.code()
        self.text ="您的资料已发送，请查收！"
        self.smtp_server = "smtp.qq.com"
        self.log=Log("email",'i')
    
    def sendmail(self,recipientAddrs,file_path, files_nameList:list[str]):
        """
        :param From: 发件人
        :param To: 接收人
        :param to_address: 接收地址
        :param subject: 邮件主题
        :param text: 邮件内容
        :param file_path: 附件路径
        :param files_name: 附件名称
        :return:
        """
        msg = MIMEMultipart()
        msg["Subject"] = files_nameList[0]+" 等文件 (自动发送)"
        msg["From"] = self.From
        msg["To"] = recipientAddrs
        text_msg = MIMEText(self.text, _charset="utf-8")
        msg.attach(text_msg)
        # smtp服务器地址
        # 收件人地址
        to_addr = recipientAddrs
        for file_name in files_nameList:
            self.log.info("正在加载附件："+file_path+file_name)
            with open(file_path+file_name, 'rb') as f:
                mime = MIMEApplication()
                mime.add_header('Content-Disposition', 'attachment', filename=file_name)
                mime.set_payload(f.read(8192))
                
                #mime.set_payload(f.read(1024 *8192))
                encoders.encode_base64(mime)
                msg.attach(mime)
    
        try:
            server = smtplib.SMTP_SSL(self.smtp_server, 465, timeout=3)  # 默认465 timeout 可写可不写
            server.login(self.from_addr,self.sercetcode)
            server.sendmail(self.from_addr, [to_addr], msg.as_string())
        except Exception as e:
            logging.error('Faild:%s' % e)
        finally:
            server.quit()
        
    