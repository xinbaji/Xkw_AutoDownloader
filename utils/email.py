import smtplib
import logging
 
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
 
 
def sendmail(self, From, To, to_address, subject, text, file_path, files_name):
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
    msg["Subject"] = subject
    msg["From"] = From
    msg["To"] = To
    text_msg = MIMEText(text, _charset="utf-8")
    msg.attach(text_msg)
    from_addr = "2417985715@qq.com"
    # smtp服务器地址
    smtp_server = "smtp.qq.com"
    # 收件人地址
    to_addr = to_address
    if file_path:
        with open(file_path, 'rb') as f:
            mime = MIMEBase('zip', 'zip')  # 发送压缩包 根绝自己发送文件的定义修改
            mime.add_header('Content-Disposition', 'attachment', filename=files_name)
            mime.add_header('Content-ID', '<0>')
            mime.add_header('X-Attachment-Id', '0')
            mime.set_payload(f.read(8192))
            
            # mime.set_payload(f.read(1024 * 8192))
            encoders.encode_base64(mime)
            msg.attach(mime)
 
    try:
        server = smtplib.SMTP_SSL(smtp_server, 465, timeout=3)  # 默认465 timeout 可写可不写
        server.login("发件人邮箱", "密码")
        server.sendmail(from_addr, [to_addr], msg.as_string())
    except Exception as e:
        logging.error('Faild:%s' % e)
    finally:
        server.quit()